# Week 3 of the DE Zoomcamp – Data Warehousing & BigQuery!

## Diving into the World of OLAP, OLTP, and BigQuery  

This week was all about **data at scale**. We explored **data warehousing, OLAP vs. OLTP, and Google BigQuery**, diving deep into **costs, best practices, and optimization techniques**. If you're working with **large datasets**, these concepts are crucial for **efficient querying, cost savings, and performance optimization**.

---

## **OLTP vs. OLAP: Understanding the Difference**  
Before jumping into BigQuery, we first differentiated **OLTP (Online Transaction Processing) and OLAP (Online Analytical Processing)**:

| Feature              | OLTP | OLAP |
|----------------------|------|------|
| **Purpose** | Runs essential business operations in real-time | Supports decision-making, problem-solving, and analytics |
| **Data updates** | Short, fast user-initiated updates | Scheduled, long-running batch jobs |
| **Database design** | Normalized for efficiency | Denormalized for analysis |
| **Space requirements** | Smaller (historical data archived) | Larger (aggregates vast amounts of data) |
| **Backup & Recovery** | Essential for business continuity | Can reload data from OLTP if needed |
| **Users** | Clerks, customer-facing staff, online shoppers | Data analysts, executives, business intelligence teams |

💡 **Takeaway:** OLTP handles real-time transactions (e.g., banking apps, e-commerce), while OLAP is for analytics and reporting (e.g., dashboards, trend analysis).

---

## **BigQuery: A Serverless Data Warehouse**  
BigQuery is a **fully managed, serverless data warehouse** that **scales automatically**. That means **no servers to manage, no infra headaches**, and **built-in high availability**.

### **Key Features:**
- **Separation of compute and storage** → Scale independently
- **On-demand & flat-rate pricing** → Pay per query or reserve capacity
- **Built-in ML & geospatial analysis** → Train models directly in BQ
- **Business intelligence (BI) integration** → Connect to Looker, Tableau, and more

### **BigQuery Pricing** 💰
| Pricing Model | Cost |
|--------------|------|
| **On-demand** | $5 per TB processed |
| **Flat rate** | $2,000/month for 100 slots (~400TB equivalent) |

💡 **Pro Tip:** **Always estimate query costs** before running them to avoid unexpected charges.

---

## **Partitioning & Clustering in BigQuery**
Optimizing queries in BigQuery requires **smart data organization**. Two key techniques:

### **Partitioning** 📌
- **Types:** Time-unit (daily, hourly, monthly), ingestion time, integer range
- **Limit:** Max **4,000 partitions** per table
- **Best for:** Filtering on a single column (e.g., date-based queries)

### **Clustering** 🔥
- **Uses multiple columns to group data together**
- **Improves filter and aggregate queries**
- **Can be applied to:** `DATE`, `BOOL`, `INT64`, `STRING`, etc.
- **Best for:** Multi-column queries and high-cardinality datasets

💡 **Choosing the Right Strategy:**  

| When to Use | Partitioning | Clustering |
|------------|-------------|-----------|
| **Cost control** | ✅ | ❌ |
| **Querying multiple columns** | ❌ | ✅ |
| **Filter/aggregate on one column** | ✅ | ❌ |
| **High cardinality datasets** | ❌ | ✅ |

### **Automatic Reclustering** 🔄
BigQuery **automatically re-clusters** tables in the background, maintaining efficient query performance without manual intervention.

---

## **BigQuery Best Practices**
### **Cost Reduction Strategies:**
✅ **Avoid `SELECT *`** – Query only necessary columns  
✅ **Use partitioned/clustered tables** – Faster, cheaper queries  
✅ **Stream inserts with caution** – Avoid unnecessary real-time data loads  
✅ **Materialize query results** – Store intermediate results instead of recomputing  

### **Performance Optimization:**
✅ **Filter on partitioned columns** – Use partition filters in WHERE clauses  
✅ **Denormalize data** – Reduce expensive JOINs when possible  
✅ **Use nested/repeated columns** – Optimize for analytics  
✅ **Optimize JOIN order** – Start with the largest table, then smaller ones  
✅ **Avoid JavaScript UDFs** – They can slow down queries significantly  

💡 **Golden Rule:** **"Just because you can run a query doesn't mean you should."** Optimize before you execute! 🚀

---

## **Final Thoughts & Gratitude** 🎉
BigQuery is **powerful**, but with great power comes **great responsibility (and costs!)**. Learning how to **structure, query, and optimize data effectively** is essential for any **data engineer** working with large-scale datasets.

A huge thank you to **Alexey Grigorev** and the **DataTalks.Club** team for making this journey possible! Their patience and dedication to answering our endless Slack questions make learning **so much more enjoyable**. 🙌


On to **Week 4!** 🚀


