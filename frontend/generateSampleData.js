#!/usr/bin/env node
// Fabricated sales data generator for RetailIQ
// Usage: node generateSampleData.js --transactions 1000 --start 2024-01-01 --end 2024-06-30 --products 20 --categories 5 --output data/fabricated_sales_data.csv

import fs from "fs";
import path from "path";
import minimist from "minimist";
import { fileURLToPath } from "url";
import { dirname } from "path";

// --- Parse CLI arguments ---
const args = minimist(process.argv.slice(2));

const NUM_TRANSACTIONS = parseInt(args.transactions) || 1000;
const START_DATE = args.start ? new Date(args.start) : new Date("2024-01-01");
const END_DATE = args.end ? new Date(args.end) : new Date("2024-03-31");
const NUM_PRODUCTS = parseInt(args.products) || 10;
const NUM_CATEGORIES = parseInt(args.categories) || 3;
const OUTPUT = args.output || "data/fabricated_sales_data.csv";

// --- Generate product and category lists ---
const categories = Array.from(
  { length: NUM_CATEGORIES },
  (_, i) => `Category${i + 1}`
);
const products = Array.from({ length: NUM_PRODUCTS }, (_, i) => ({
  name: `Product${i + 1}`,
  category: categories[i % NUM_CATEGORIES],
  basePrice: Math.round((Math.random() * 90 + 10) * 100) / 100, // $10-$100
}));

// --- Helper functions ---
function randomDate(start, end) {
  return new Date(
    start.getTime() + Math.random() * (end.getTime() - start.getTime())
  );
}
function pad(n) {
  return n < 10 ? "0" + n : n;
}
function formatDate(d) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// --- Generate transactions ---
let csvRows = ["TransactionID,Date,Product,Units Sold,Price,Category"];
let transactionId = 100000;

for (let i = 0; i < NUM_TRANSACTIONS; i++) {
  // Simulate a basket (1-5 items per transaction)
  const basketSize = randomInt(1, 5);
  const date = randomDate(START_DATE, END_DATE);
  const tid = transactionId++;
  const chosenProducts = [];
  while (chosenProducts.length < basketSize) {
    const p = products[randomInt(0, products.length - 1)];
    if (!chosenProducts.includes(p)) chosenProducts.push(p);
  }
  for (const p of chosenProducts) {
    const units = randomInt(1, 5);
    const price =
      Math.round(p.basePrice * (0.8 + Math.random() * 0.4) * 100) / 100; // 80-120% of base
    csvRows.push(
      [tid, formatDate(date), p.name, units, price, p.category].join(",")
    );
  }
}

// --- Write to file ---

// For ESM __dirname compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const outPath = path.resolve(__dirname, OUTPUT);
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, csvRows.join("\n"));
console.log(`Generated ${NUM_TRANSACTIONS} transactions to ${outPath}`);

// --- Dependency note ---
// Requires 'minimist' (install with: npm install minimist)
