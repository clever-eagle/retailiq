import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")


class SalesForecaster:
    """
    Sales Forecasting using multiple models
    Supports Linear Regression, Random Forest, ARIMA, and Exponential Smoothing
    """

    def __init__(self):
        self.models = {}
        self.model_performance = {}
        self.label_encoders = {}

    def prepare_time_series_data(self, df, product_filter=None, category_filter=None):
        """
        Prepare data for time series forecasting
        """
        try:
            # Make a copy to avoid modifying original data
            data = df.copy()

            # Convert date column to datetime
            if "date" in data.columns:
                data["date"] = pd.to_datetime(data["date"])
            else:
                raise ValueError("Date column not found in data")

            # Apply filters
            if product_filter:
                data = data[data["product_name"] == product_filter]
            if category_filter:
                data = data[data["category"] == category_filter]

            if data.empty:
                raise ValueError("No data available after applying filters")

            # Aggregate by date
            if "total_amount" in data.columns:
                daily_sales = (
                    data.groupby("date")
                    .agg(
                        {
                            "total_amount": "sum",
                            "quantity": "sum",
                            "transaction_id": "nunique",
                        }
                    )
                    .reset_index()
                )
            else:
                # Calculate total_amount if not present
                data["total_amount"] = data["quantity"] * data["unit_price"]
                daily_sales = (
                    data.groupby("date")
                    .agg(
                        {
                            "total_amount": "sum",
                            "quantity": "sum",
                            "transaction_id": "nunique",
                        }
                    )
                    .reset_index()
                )

            daily_sales.columns = ["date", "revenue", "quantity_sold", "transactions"]
            daily_sales = daily_sales.sort_values("date")

            # Fill missing dates with zero sales
            date_range = pd.date_range(
                start=daily_sales["date"].min(), end=daily_sales["date"].max(), freq="D"
            )

            complete_dates = pd.DataFrame({"date": date_range})
            daily_sales = complete_dates.merge(daily_sales, on="date", how="left")
            daily_sales = daily_sales.fillna(0)

            return daily_sales

        except Exception as e:
            print(f"Error preparing time series data: {e}")
            return pd.DataFrame()

    def create_features(self, df):
        """
        Create features for machine learning models
        """
        try:
            data = df.copy()

            # Extract date features
            data["year"] = data["date"].dt.year
            data["month"] = data["date"].dt.month
            data["day"] = data["date"].dt.day
            data["day_of_week"] = data["date"].dt.dayofweek
            data["day_of_year"] = data["date"].dt.dayofyear
            data["week_of_year"] = data["date"].dt.isocalendar().week

            # Create lag features
            for lag in [1, 3, 7, 14, 30]:
                data[f"revenue_lag_{lag}"] = data["revenue"].shift(lag)
                data[f"quantity_lag_{lag}"] = data["quantity_sold"].shift(lag)

            # Create rolling window features
            for window in [3, 7, 14, 30]:
                data[f"revenue_rolling_mean_{window}"] = (
                    data["revenue"].rolling(window=window).mean()
                )
                data[f"revenue_rolling_std_{window}"] = (
                    data["revenue"].rolling(window=window).std()
                )
                data[f"quantity_rolling_mean_{window}"] = (
                    data["quantity_sold"].rolling(window=window).mean()
                )

            # Create trend features
            data["revenue_trend"] = data["revenue"].diff()
            data["quantity_trend"] = data["quantity_sold"].diff()

            # Fill NaN values
            data = data.fillna(method="bfill").fillna(0)

            return data

        except Exception as e:
            print(f"Error creating features: {e}")
            return df

    def train_linear_regression(self, train_data, target_column="revenue"):
        """
        Train Linear Regression model
        """
        try:
            feature_columns = [
                col for col in train_data.columns if col not in ["date", target_column]
            ]

            X = train_data[feature_columns]
            y = train_data[target_column]

            model = LinearRegression()
            model.fit(X, y)

            # Make predictions on training data for performance evaluation
            y_pred = model.predict(X)

            performance = {
                "mae": mean_absolute_error(y, y_pred),
                "rmse": np.sqrt(mean_squared_error(y, y_pred)),
                "r2": r2_score(y, y_pred),
            }

            return model, performance, feature_columns

        except Exception as e:
            print(f"Error training linear regression: {e}")
            return None, {}, []

    def train_random_forest(self, train_data, target_column="revenue"):
        """
        Train Random Forest model
        """
        try:
            feature_columns = [
                col for col in train_data.columns if col not in ["date", target_column]
            ]

            X = train_data[feature_columns]
            y = train_data[target_column]

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)

            # Make predictions on training data for performance evaluation
            y_pred = model.predict(X)

            performance = {
                "mae": mean_absolute_error(y, y_pred),
                "rmse": np.sqrt(mean_squared_error(y, y_pred)),
                "r2": r2_score(y, y_pred),
            }

            return model, performance, feature_columns

        except Exception as e:
            print(f"Error training random forest: {e}")
            return None, {}, []

    def train_arima(self, train_data, target_column="revenue"):
        """
        Train ARIMA model
        """
        try:
            ts_data = train_data.set_index("date")[target_column]

            # Use auto ARIMA parameters (simple approach)
            model = ARIMA(ts_data, order=(1, 1, 1))
            fitted_model = model.fit()

            # Get fitted values for performance evaluation
            y_pred = fitted_model.fittedvalues
            y_true = ts_data

            # Align the series (fitted values might be shorter)
            min_len = min(len(y_pred), len(y_true))
            y_pred = y_pred[-min_len:]
            y_true = y_true[-min_len:]

            performance = {
                "mae": mean_absolute_error(y_true, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
                "r2": r2_score(y_true, y_pred) if len(y_true) > 1 else 0,
            }

            return fitted_model, performance

        except Exception as e:
            print(f"Error training ARIMA: {e}")
            return None, {}

    def forecast(self, df, forecast_days=30, product_filter=None, category_filter=None):
        """
        Generate sales forecast using multiple models
        """
        try:
            # Prepare data
            time_series_data = self.prepare_time_series_data(
                df, product_filter, category_filter
            )

            if time_series_data.empty:
                return {"error": "No data available for forecasting"}

            # Create features
            featured_data = self.create_features(time_series_data)

            # Split data (use 80% for training)
            split_idx = int(len(featured_data) * 0.8)
            train_data = featured_data[:split_idx]
            test_data = featured_data[split_idx:]

            results = {
                "historical_data": [],
                "forecasts": {},
                "model_performance": {},
                "metadata": {
                    "forecast_days": forecast_days,
                    "training_period": {
                        "start": train_data["date"].min().isoformat(),
                        "end": train_data["date"].max().isoformat(),
                    },
                    "data_points": len(featured_data),
                },
            }

            # Prepare historical data for response
            for _, row in time_series_data.iterrows():
                results["historical_data"].append(
                    {
                        "date": row["date"].isoformat(),
                        "revenue": float(row["revenue"]),
                        "quantity_sold": int(row["quantity_sold"]),
                        "transactions": int(row["transactions"]),
                    }
                )

            # Train models and generate forecasts

            # 1. Linear Regression
            try:
                lr_model, lr_performance, feature_cols = self.train_linear_regression(
                    train_data
                )
                if lr_model is not None:
                    results["model_performance"]["linear_regression"] = lr_performance
                    lr_forecast = self._generate_ml_forecast(
                        lr_model, featured_data, feature_cols, forecast_days
                    )
                    results["forecasts"]["linear_regression"] = lr_forecast
            except Exception as e:
                print(f"Linear regression forecast failed: {e}")

            # 2. Random Forest
            try:
                rf_model, rf_performance, feature_cols = self.train_random_forest(
                    train_data
                )
                if rf_model is not None:
                    results["model_performance"]["random_forest"] = rf_performance
                    rf_forecast = self._generate_ml_forecast(
                        rf_model, featured_data, feature_cols, forecast_days
                    )
                    results["forecasts"]["random_forest"] = rf_forecast
            except Exception as e:
                print(f"Random forest forecast failed: {e}")

            # 3. Simple moving average (fallback)
            try:
                ma_forecast = self._generate_moving_average_forecast(
                    time_series_data, forecast_days
                )
                results["forecasts"]["moving_average"] = ma_forecast
            except Exception as e:
                print(f"Moving average forecast failed: {e}")

            # Add ensemble forecast (average of available forecasts)
            if results["forecasts"]:
                results["forecasts"]["ensemble"] = self._create_ensemble_forecast(
                    results["forecasts"], forecast_days
                )

            return results

        except Exception as e:
            print(f"Error in forecasting: {e}")
            return {"error": str(e)}

    def _generate_ml_forecast(self, model, data, feature_cols, forecast_days):
        """
        Generate forecast using machine learning model
        """
        try:
            last_date = data["date"].max()
            forecast_dates = [
                last_date + timedelta(days=i + 1) for i in range(forecast_days)
            ]

            forecasts = []

            # Use last known values for lag features
            last_row = data.iloc[-1].copy()

            for i, forecast_date in enumerate(forecast_dates):
                # Create features for forecast date
                forecast_row = last_row.copy()
                forecast_row["date"] = forecast_date
                forecast_row["year"] = forecast_date.year
                forecast_row["month"] = forecast_date.month
                forecast_row["day"] = forecast_date.day
                forecast_row["day_of_week"] = forecast_date.weekday()
                forecast_row["day_of_year"] = forecast_date.timetuple().tm_yday
                forecast_row["week_of_year"] = forecast_date.isocalendar()[1]

                # Make prediction
                X = forecast_row[feature_cols].values.reshape(1, -1)
                prediction = model.predict(X)[0]

                forecasts.append(
                    {
                        "date": forecast_date.isoformat(),
                        "predicted_revenue": max(
                            0, float(prediction)
                        ),  # Ensure non-negative
                        "confidence_interval": {
                            "lower": max(0, float(prediction * 0.8)),
                            "upper": float(prediction * 1.2),
                        },
                    }
                )

                # Update last_row for next iteration
                last_row["revenue"] = prediction

            return forecasts

        except Exception as e:
            print(f"Error generating ML forecast: {e}")
            return []

    def _generate_moving_average_forecast(self, data, forecast_days, window=7):
        """
        Generate forecast using moving average
        """
        try:
            last_values = data["revenue"].tail(window).mean()
            last_date = data["date"].max()

            forecasts = []
            for i in range(forecast_days):
                forecast_date = last_date + timedelta(days=i + 1)
                forecasts.append(
                    {
                        "date": forecast_date.isoformat(),
                        "predicted_revenue": float(last_values),
                        "confidence_interval": {
                            "lower": float(last_values * 0.7),
                            "upper": float(last_values * 1.3),
                        },
                    }
                )

            return forecasts

        except Exception as e:
            print(f"Error generating moving average forecast: {e}")
            return []

    def _create_ensemble_forecast(self, forecasts, forecast_days):
        """
        Create ensemble forecast by averaging multiple model predictions
        """
        try:
            ensemble_forecasts = []

            for i in range(forecast_days):
                predictions = []

                for model_name, model_forecasts in forecasts.items():
                    if model_name != "ensemble" and i < len(model_forecasts):
                        predictions.append(model_forecasts[i]["predicted_revenue"])

                if predictions:
                    avg_prediction = np.mean(predictions)
                    std_prediction = np.std(predictions) if len(predictions) > 1 else 0

                    # Use first forecast's date
                    forecast_date = list(forecasts.values())[0][i]["date"]

                    ensemble_forecasts.append(
                        {
                            "date": forecast_date,
                            "predicted_revenue": float(avg_prediction),
                            "confidence_interval": {
                                "lower": max(0, float(avg_prediction - std_prediction)),
                                "upper": float(avg_prediction + std_prediction),
                            },
                        }
                    )

            return ensemble_forecasts

        except Exception as e:
            print(f"Error creating ensemble forecast: {e}")
            return []

    def get_trends(self, df):
        """
        Analyze sales trends
        """
        try:
            time_series_data = self.prepare_time_series_data(df)

            if time_series_data.empty:
                return {"error": "No data available for trends analysis"}

            # Calculate basic trends
            total_revenue = time_series_data["revenue"].sum()
            avg_daily_revenue = time_series_data["revenue"].mean()
            revenue_growth = time_series_data["revenue"].pct_change().mean() * 100

            # Get top performing days
            top_days = time_series_data.nlargest(5, "revenue")[
                ["date", "revenue"]
            ].to_dict("records")
            for day in top_days:
                day["date"] = day["date"].isoformat()

            # Monthly trends
            time_series_data["month_year"] = time_series_data["date"].dt.to_period("M")
            monthly_trends = (
                time_series_data.groupby("month_year")
                .agg({"revenue": "sum", "quantity_sold": "sum", "transactions": "sum"})
                .reset_index()
            )

            monthly_trends["month_year"] = monthly_trends["month_year"].astype(str)
            monthly_data = monthly_trends.to_dict("records")

            # Weekly patterns
            time_series_data["day_of_week"] = time_series_data["date"].dt.day_name()
            weekly_patterns = (
                time_series_data.groupby("day_of_week")["revenue"].mean().to_dict()
            )

            return {
                "summary": {
                    "total_revenue": float(total_revenue),
                    "avg_daily_revenue": float(avg_daily_revenue),
                    "revenue_growth_rate": (
                        float(revenue_growth) if not np.isnan(revenue_growth) else 0
                    ),
                    "date_range": {
                        "start": time_series_data["date"].min().isoformat(),
                        "end": time_series_data["date"].max().isoformat(),
                    },
                },
                "top_performing_days": top_days,
                "monthly_trends": monthly_data,
                "weekly_patterns": weekly_patterns,
            }

        except Exception as e:
            print(f"Error analyzing trends: {e}")
            return {"error": str(e)}
