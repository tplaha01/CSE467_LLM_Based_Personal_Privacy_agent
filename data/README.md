The current `ground_truth.csv` and `statements.csv` were converted from the teammate annotation workbook `annotation_devashish.xlsx`, sheet `annotations`. The workbook contained 50 rows with `item_id`, `statement`, and the seven required harm labels. `item_id` was renamed to `statement_id` without changing labels.

Inference reads only `statement_id` and `statement`; labels are loaded only by evaluation. Replace this dataset only through an agreed annotation/reconciliation process.
