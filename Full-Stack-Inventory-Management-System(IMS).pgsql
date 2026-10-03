Full-Stack-Inventory-Management-System(IMS)  
├── Frontend/ (React • JavaScript • HTML • CSS) components -> pages -> hooks -> services -> routes -> utils -> App.jsx
│   │
│   ├── index.html
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── logo.png
│   ├── src/
│   │   ├── assets/                                         
│   │   │   ├── icons/                                 
│   │   │   ├── images/                             
│   │   │   ├── fonts/
│   │   │   └── styles/  
│   │   │       ├── global.css
│   │   │       ├── variables.css
│   │   │       ├── reset.css
│   │   │       └── typography.css                        
│   │   │
│   │   ├── components/                                     
│   │   │   ├── ui/  
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Input.jsx 
│   │   │   │   ├── Select.jsx 
│   │   │   │   ├── Modal.jsx 
│   │   │   │   ├── Table.jsx 
│   │   │   │   ├── Badge.jsx 
│   │   │   │   ├── Spinner.jsx 
│   │   │   │   ├── Pagination.jsx 
│   │   │   │   ├── Alert.jsx
│   │   │   │   └── Card.jsx      
│   │   │   ├── layout/
│   │   │   │   ├── AppLayout.jsx 
│   │   │   │   ├── Sidebar.jsx 
│   │   │   │   ├── Navbar.jsx 
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── PageHeader.jsx      
│   │   │   └── common/
│   │   │       ├── EmptyState.jsx
│   │   │       ├── ErrorState.jsx  
│   │   │       ├── LoadingState.jsx
│   │   │       └── ConfirmDialog.jsx
│   │   │  
│   │   ├── features/                                       
│   │   │      ├── auth/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── LoginForm.jsx
│   │   │  	│	│   ├── RegisterForm.jsx 
│   │   │  	│	│   ├── ForgotPasswordForm.jsx 
│   │   │  	│	│   ├── ResetPasswordForm.jsx 
│   │   │      │    │   └── ProtectedRoute.jsx 
│   │   │  	│	├── pages/                               
│   │   │  	│	│   ├── Login.jsx 
│   │   │  	│	│   ├── Register.jsx 
│   │   │  	│	│   ├── ForgotPassword.jsx 
│   │   │      │    │   └── ResetPassword.jsx 
│   │   │  	│	├── hooks/                               
│   │   │      │    │   └── useAuth.jsx
│   │   │  	│	├── context/                             
│   │   │      │    │   └── index.js
│   │   │  	│	├── services/                            
│   │   │      │    │   └── authService.js 
│   │   │  	│	├── utils/                               
│   │   │  	│	│   ├── authHelpers.js
│   │   │  	│	│   ├── authValidators.js
│   │   │  	│	│   ├── authMapper.js 
│   │   │  	│	│   ├── authStorage.js
│   │   │      │    │   └── index.js
│   │   │  	│	├── validation/                              
│   │   │      │    │   └── authValidation.js
│   │   │      │    └── index.js
│   │   │      │
│   │   │      ├── dashboard/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── StateCard.jsx
│   │   │  	│	│   ├── SalesChart.jsx 
│   │   │  	│	│   ├── InventoryChart.jsx 
│   │   │  	│	│   ├── LowStockList.jsx 
│   │   │  	│	│   ├── RecentTransactions.jsx
│   │   │  	│	│   ├── RecentSales.jsx
│   │   │      │    │   └── TopProducts.jsx 
│   │   │  	│	├── pages/                               
│   │   │      │    │   └── Dashboard.jsx 
│   │   │  	│	├── hooks/                               
│   │   │      │    │   └── useDashboard.jsx
│   │   │  	│	├── services/                            
│   │   │      │    │   └── dashboardService.js 
│   │   │  	│	├── utils/                               
│   │   │      │    │   └── udashboardUtils.js 
│   │   │      │    └── index.js
│   │   │      │
│   │   │      ├── products/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── ProductTable.jsx
│   │   │  	│	│   ├── ProductForm.jsx 
│   │   │  	│	│   ├── ProductCard.jsx 
│   │   │  	│	│   ├── ProductDetails.jsx 
│   │   │  	│	│   ├── ProductSearch.jsx
│   │   │  	│	│   ├── ProductFilters.jsx
│   │   │  	│	│   ├── ProductStatus.jsx
│   │   │      │    │   └── ProductDeleteDialog.jsx 
│   │   │  	│	├── pages/                               
│   │   │  	│	│   ├── Products.jsx 
│   │   │  	│	│   ├── AddProduct.jsx 
│   │   │  	│	│   ├── EditProduct.jsx 
│   │   │      │    │   └── ProductView.jsx 
│   │   │  	│	├── hooks/                               
│   │   │      │    │   └── useProducts.js
│   │   │  	│	├── services/                            
│   │   │      │    │   └── productService.js 
│   │   │  	│	├── validation/                               
│   │   │      │    │   └── productValidation.js 
│   │   │  	│	├── utils/                              
│   │   │      │    │   └── productUtils.js
│   │   │      │    └── index.js
│   │   │      │
│   │   │      ├── suppliers/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── SupplierTable.jsx
│   │   │  	│	│   ├── SupplierForm.jsx 
│   │   │  	│	│   ├── SupplierDetails.jsx 
│   │   │  	│	│   ├── SupplierCard.jsx 
│   │   │  	│	│   ├── SupplierStatus.jsx
│   │   │  	│	│   ├── SupplierSearch.jsx
│   │   │  	│	│   ├── SupplierFilters.jsx
│   │   │  	│	│   ├── SupplierProducts.jsx
│   │   │  	│	│   ├── SupplierPurchaseHistory.jsx
│   │   │  	│	│   ├── SupplierPaymentInfo.jsx
│   │   │      │    │   └── SupplierDeleteDialog.jsx 
│   │   │  	│	├── pages/                               
│   │   │  	│	│   ├── Suppliers.jsx 
│   │   │  	│	│   ├── AddSupplier.jsx 
│   │   │  	│	│   ├── EditSupplier.jsx 
│   │   │  	│	│   ├── SupplierView.jsx 
│   │   │  	│	│   ├── SupplierProductsPage.jsx
│   │   │      │    │   └── SupplierHistory.jsx 
│   │   │  	│	├── hooks/                               
│   │   │      │    │   └── useSuppliers.js
│   │   │  	│	├── services/                            
│   │   │      │    │   └── supplierService.js 
│   │   │  	│	├── validation/                               
│   │   │      │    │   └── supplierValidation.js 
│   │   │  	│	├── utils/                              
│   │   │      │    │   └── supplierUtils.js
│   │   │      │    └── index.js
│   │   │      │
│   │   │      ├── inventory/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── InventoryTable.jsx
│   │   │  	│	│   ├── InventoryCard.jsx 
│   │   │  	│	│   ├── StockStatus.jsx 
│   │   │  	│	│   ├── StockInForm.jsx 
│   │   │  	│	│   ├── StockOutForm.jsx
│   │   │  	│	│   ├── StockAdjustmentForm.jsx
│   │   │  	│	│   ├── StockTransferForm.jsx
│   │   │  	│	│   ├── InventoryFilters.jsx
│   │   │  	│	│   ├── InventorySearch.jsx
│   │   │  	│	│   ├── LowStockAlert.jsx
│   │   │      │    │   └── TransactionHistory.jsx 
│   │   │  	│	├── pages/                               
│   │   │  	│	│   ├── Inventory.jsx 
│   │   │  	│	│   ├── StockIn.jsx 
│   │   │  	│	│   ├── StockOut.jsx 
│   │   │  	│	│   ├── StockAdjustment.jsx 
│   │   │  	│	│   ├── StockTransfer.jsx 
│   │   │      │    │   └── InventoryHistory.jsx 
│   │   │  	│	├── hooks/                               
│   │   │      │    │   └── useInventory.js 
│   │   │  	│	├── services/                            
│   │   │      │    │   └── inventoryService.js 
│   │   │  	│	├── utils/                              
│   │   │      │    │   └── inventoryUtils.js
│   │   │      │    └── index.js
│   │   │      │
│   │   │      ├── purchases/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── PurchaseTable.jsx
│   │   │  	│	│   ├── PurchaseForm.jsx 
│   │   │  	│	│   ├── PurchaseDetails.jsx 
│   │   │  	│	│   ├── PurchaseItemForm.jsx 
│   │   │  	│	│   ├── PurchaseItemTable.jsx
│   │   │  	│	│   ├── SupplierSelect.jsx
│   │   │  	│	│   ├── PurchaseStatus.jsx
│   │   │  	│	│   ├── PaymentStatus.jsx
│   │   │  	│	│   ├── ReceivePurchaseForm.jsx
│   │   │  	│	│   ├── PurchaseFilters.jsx
│   │   │      │    │   └── PurchaseDeleteDialog.jsx 
│   │   │      │    │
│   │   │  	│	├── pages/                               
│   │   │  	│	│   ├── Purchase.jsx 
│   │   │  	│	│   ├── CreatePurchase.jsx 
│   │   │  	│	│   ├── EditPurchase.jsx 
│   │   │  	│	│   ├── PurchaseView.jsx  
│   │   │      │    │   └── ReceivePurchase.jsx 
│   │   │      │    │
│   │   │  	│	├── hooks/                               
│   │   │      │    │   └── usePurchases.js 
│   │   │  	│	├── services/                            
│   │   │      │    │   └── purchaseService.js
│   │   │  	│	├── validation/                            
│   │   │      │    │   └── purchaseValidation.js 
│   │   │  	│	├── utils/                              
│   │   │      │    │   └── purchaseUtils.js
│   │   │      │    └── index.js
│   │   │      │
│   │   │      ├── sales/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── SalesTable.jsx
│   │   │  	│	│   ├── SalesForm.jsx 
│   │   │  	│	│   ├── SalesDetails.jsx 
│   │   │  	│	│   ├── SalesItemForm.jsx 
│   │   │  	│	│   ├── SalesItemTable.jsx 
│   │   │  	│	│   ├── CustomerSelect.jsx
│   │   │  	│	│   ├── ProductSelect.jsx
│   │   │  	│	│   ├── SalesStatus.jsx
│   │   │  	│	│   ├── PaymentStatus.jsx
│   │   │  	│	│   ├── PaymentForm.jsx
│   │   │  	│	│   ├── InvoicePreview.jsx
│   │   │  	│	│   ├── SalesFilters.jsx 
│   │   │      │    │   └── SalesDeleteDialog.jsx  
│   │   │  	│	├── pages/                               
│   │   │  	│	│   ├── Sales.jsx 
│   │   │  	│	│   ├── CreateSale.jsx 
│   │   │  	│	│   ├── EditSale.jsx 
│   │   │  	│	│   ├── SaleView.jsx 
│   │   │  	│	│   ├── Invoice.jsx 
│   │   │      │    │   └── Payments.jsx 
│   │   │  	│	├── hooks/                               
│   │   │      │    │   └── useSales.js 
│   │   │  	│	├── services/                            
│   │   │      │    │   └── salesService.js 
│   │   │  	│	├── validation/                              
│   │   │      │    │   └── salesValidation.js
│   │   │  	│	├── utils/                              
│   │   │      │    │   └── salesUtils.js
│   │   │      │    └── index.js
│   │   │      │
│   │   │      ├── reports/ 
│   │   │  	│	├── components/                         
│   │   │  	│	│   ├── ReportCard.jsx
│   │   │  	│	│   ├── ReportHeader.jsx 
│   │   │  	│	│   ├── ReportFilters.jsx 
│   │   │  	│	│   ├── DateRangePicker.jsx 
│   │   │  	│	│   ├── SalesChart.jsx
│   │   │  	│	│   ├── PurchaseChart.jsx
│   │   │  	│	│   ├── InventoryChart.jsx
│   │   │  	│	│   ├── ProfileChart.jsx
│   │   │  	│	│   ├── StockMovementChart.jsx
│   │   │  	│	│   ├── ReportTable.jsx
│   │   │  	│	│   ├── ReportSummary.jsx 
│   │   │      │    │   └── TransactionHistory.jsx 
│   │   │      │    │
│   │   │  	│	├── pages/                               
│   │   │  	│	│   ├── Reports.jsx 
│   │   │  	│	│   ├── SalesReport.jsx 
│   │   │  	│	│   ├── PurchaseReport.jsx 
│   │   │  	│	│   ├── InventoryReport.jsx 
│   │   │  	│	│   ├── ProfileReport.jsx 
│   │   │  	│	│   ├── StockMovementReport.jsx
│   │   │      │    │   └── ProductPerformanceReport.jsx 
│   │   │      │    │
│   │   │      │	├── hooks/                               
│   │   │      │    │   └── useReports.js 
│   │   │      │    ├── services/                            
│   │   │      │    │   └── reportService.js 
│   │   │      │	├── utils/                              
│   │   │      │    │   └── reportUtils.js
│   │   │      │    └── index.js
│   │   │      │
│   │   │      └── users/
│   │   │  		├── components/                         
│   │   │  		│   ├── UserTable.jsx
│   │   │  		│   ├── UserForm.jsx 
│   │   │  		│   ├── UserDetails.jsx 
│   │   │  		│   ├── UserAvatar.jsx 
│   │   │  		│   ├── UserStatus.jsx
│   │   │  		│   ├── PermissionList.jsx
│   │   │  		│   ├── UserFilters.jsx
│   │   │  		│   ├── UserSearch.jsx
│   │   │  		│   ├── ChangePasswordForm.jsx
│   │   │  		│   ├── UserActivity.jsx
│   │   │           │   └── UserDeleteDialog.jsx 
│   │   │  		├── pages/                               
│   │   │  		│   ├── Users.jsx 
│   │   │  		│   ├── AddUser.jsx 
│   │   │  		│   ├── EditUser.jsx 
│   │   │  		│   ├── UserView.jsx 
│   │   │  		│   ├── Roles.jsx 
│   │   │           │   └── UserProfile.jsx 
│   │   │  		├── hooks/                               
│   │   │           │   └── useUsers.js 
│   │   │  		├── services/                            
│   │   │           │   └── userService.js 
│   │   │  		├── utils/                              
│   │   │           │   └── userUtils.js
│   │   │           └── index.js
│   │   │
│   │   ├── hooks/                                       
│   │   │   ├── useDebounce.js                              
│   │   │   ├── usePagination.js                             
│   │   │   └── useModal.js
│   │   │
│   │   ├── services/                                    
│   │   │   ├── api.js                                   
│   │   │   └── uploadService.js 
│   │   │
│   │   ├── routes/                                  
│   │   │   ├── AppRoutes.jsx                        
│   │   │   ├── PrivateRoutes.jsx                            
│   │   │   └── routeConfig.js                                 
│   │   │
│   │   ├── utils/                                                                
│   │   │   ├── constants.js 
│   │   │   ├── formatters.js                             
│   │   │   ├── dateUtils.js                            
│   │   │   ├── currencyUtils.js                                                        
│   │   │   └── storage.js                         
│   │   │      
│   │   ├── App.jsx 
│   │   ├── main.jsx                                    
│   │   └── index.css    
│   │
│   ├── .env 
│   ├── .env.example 
│   ├── package.json                     
│   └── README.md           
│                            
├──Backend/
│    ├── app/
│    │   ├── __init__.py
│    │   ├── main.py
│    │   │
│    │   ├── core/
│    │   │   ├── __init__.py
│    │   │   ├── config.py
│    │   │   ├── database.py
│    │   │   ├── security.py
│    │   │   ├── permissions.py
│    │   │   ├── exceptions.py
│    │   │   └── logging.py
│    │   │
│    │   ├── models/
│    │   │   ├── __init__.py
│    │   │   ├── user.py
│    │   │   ├── role.py
│    │   │   ├── permission.py
│    │   │   ├── category.py
│    │   │   ├── product.py
│    │   │   ├── supplier.py
│    │   │   ├── customer.py
│    │   │   ├── inventory.py
│    │   │   ├── inventory_transaction.py
│    │   │   ├── purchase.py
│    │   │   ├── purchase_item.py
│    │   │   ├── sale.py
│    │   │   ├── sale_item.py
│    │   │   └── payment.py
│    │   │
│    │   ├── schemas/
│    │   │   ├── __init__.py
│    │   │   ├── auth.py
│    │   │   ├── user.py
│    │   │   ├── category.py
│    │   │   ├── product.py
│    │   │   ├── supplier.py
│    │   │   ├── customer.py
│    │   │   ├── inventory.py
│    │   │   ├── purchase.py
│    │   │   ├── sale.py
│    │   │   ├── payment.py
│    │   │   ├── dashboard.py
│    │   │   └── report.py
│    │   │
│    │   ├── api/
│    │   │   ├── __init__.py
│    │   │   ├── dependencies.py
│    │   │   └── v1/
│    │   │       ├── __init__.py
│    │   │       ├── router.py
│    │   │       ├── auth.py
│    │   │       ├── users.py
│    │   │       ├── products.py
│    │   │       ├── categories.py
│    │   │       ├── suppliers.py
│    │   │       ├── customers.py
│    │   │       ├── inventory.py
│    │   │       ├── purchases.py
│    │   │       ├── sales.py
│    │   │       ├── payments.py
│    │   │       ├── dashboard.py
│    │   │       └── reports.py
│    │   │
│    │   ├── services/
│    │   │   ├── __init__.py
│    │   │   ├── auth_service.py
│    │   │   ├── user_service.py
│    │   │   ├── product_service.py
│    │   │   ├── supplier_service.py
│    │   │   ├── customer_service.py
│    │   │   ├── inventory_service.py
│    │   │   ├── purchase_service.py
│    │   │   ├── sales_service.py
│    │   │   ├── payment_service.py
│    │   │   ├── dashboard_service.py
│    │   │   └── report_service.py
│    │   │
│    │   ├── repositories/
│    │   │   ├── __init__.py
│    │   │   ├── user_repository.py
│    │   │   ├── product_repository.py
│    │   │   ├── supplier_repository.py
│    │   │   ├── customer_repository.py
│    │   │   ├── inventory_repository.py
│    │   │   ├── purchase_repository.py
│    │   │   └── sales_repository.py
│    │   │
│    │   ├── utils/
│    │   │   ├── __init__.py
│    │   │   ├── pagination.py
│    │   │   ├── validators.py
│    │   │   ├── formatters.py
│    │   │   ├── invoice.py
│    │   │   └── helpers.py
│    │   │
│    │   └── middleware/
│    │       ├── __init__.py
│    │       ├── cors.py
│    │       ├── error_handler.py
│    │       └── request_logging.py
│    │
│    ├── alembic/
│    │   ├── versions/
│    │   └── env.py
│    │
│    ├── tests/
│    │   ├── __init__.py
│    │   ├── conftest.py
│    │   ├── test_auth.py
│    │   ├── test_products.py
│    │   ├── test_inventory.py
│    │   ├── test_purchases.py
│    │   └── test_sales.py
│    │
│    ├── uploads/
│    ├── .env
│    ├── .env.example
│    ├── alembic.ini
│    ├── requirements.txt
│    ├── pyproject.toml
│    └── README.md


                    INVENTORY MANAGEMENT SYSTEM
                              │
             ┌────────────────┴────────────────┐
             │                                 │
             ▼                                 ▼
      React Frontend                     Python Backend
      JavaScript                         FastAPI
             │                                 │
             │ REST / JSON                     │
             └───────────────┬─────────────────┘
                             │
                             ▼
                       PostgreSQL

