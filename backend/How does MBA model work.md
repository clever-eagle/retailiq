Here’s a detailed example of an association rule:

Suppose your dataset has many transactions like:
- Transaction 1: Bread, Butter, Milk
- Transaction 2: Bread, Butter
- Transaction 3: Bread, Milk
- Transaction 4: Butter, Milk
- Transaction 5: Bread, Butter, Milk

A possible rule is:
**If a customer buys Bread and Butter, they also buy Milk.**

- **Support:**  
  This rule appears in 3 out of 5 transactions (Transactions 1, 5, and 4).  
  Support = 3/5 = 0.6 (60%)

- **Confidence:**  
  Of all transactions where Bread and Butter are bought together (Transactions 1, 2, 5), Milk is also bought in 2 of them (Transactions 1 and 5).  
  Confidence = 2/3 ≈ 0.67 (67%)

If you set min support to 0.5 and min confidence to 0.6, this rule passes both filters and is included in the results.

**Summary:**  
- The rule describes a pattern: Bread + Butter → Milk.
- Support tells you how common this pattern is.
- Confidence tells you how reliable this pattern is.
- Only rules that meet your min support and confidence are shown.