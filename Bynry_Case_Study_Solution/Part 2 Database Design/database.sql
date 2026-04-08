CREATE TABLE companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE warehouses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID NOT NULL REFERENCES companies(id),
  name VARCHAR(255) NOT NULL,
  location VARCHAR(255)
);

CREATE TABLE suppliers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID NOT NULL REFERENCES companies(id),
  name VARCHAR(255) NOT NULL
);

CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID NOT NULL REFERENCES companies(id),
  sku VARCHAR(100) NOT NULL,
  name VARCHAR(255) NOT NULL,
  is_bundle BOOLEAN DEFAULT FALSE,
  UNIQUE(company_id, sku)
);

CREATE TABLE supplier_products (
  supplier_id UUID NOT NULL REFERENCES suppliers(id),
  product_id UUID NOT NULL REFERENCES products(id),
  supplier_sku VARCHAR(100),
  unit_cost DECIMAL(10, 2),
  PRIMARY KEY (supplier_id, product_id)
);

CREATE TABLE product_bundles (
  bundle_id UUID NOT NULL REFERENCES products(id),
  component_id UUID NOT NULL REFERENCES products(id),
  quantity INT NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (bundle_id, component_id)
);

CREATE TABLE inventory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  warehouse_id UUID NOT NULL REFERENCES warehouses(id),
  product_id UUID NOT NULL REFERENCES products(id),
  quantity INT NOT NULL DEFAULT 0,
  UNIQUE(warehouse_id, product_id)
);

CREATE TABLE inventory_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  inventory_id UUID NOT NULL REFERENCES inventory(id),
  transaction_type VARCHAR(50) NOT NULL, 
  quantity_change INT NOT NULL, 
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- -- Missing Requirements / Questions for Product:

-- Bundles: Are bundles physical pre-packaged items we track in inventory, or just logical groupings where we deduct the individual component inventory at checkout?

-- Multi-tenancy: Is this a shared database for all SaaS clients? (I assumed yes and added company_id to top-level tables).

-- Negative Inventory: Can stock levels drop below 0 to support backorders, or should the DB reject negative quantities?

-- Traceability: Do we need to track specific batches, lots, or serial numbers, or just aggregate quantities per warehouse?

-- Deletions: Should we implement soft deletes (e.g., is_active boolean) so we don't break historical transaction records when a product is discontinued?

-- Design Decisions:

-- inventory_transactions table: Solves the "track when inventory changes" requirement. It's an append-only ledger tracking the exact delta (in or out) and timestamp for every stock movement.

-- product_bundles table: Used a self-referencing many-to-many relationship. A product can be made of other products, and this tracks exactly which components and how many are needed.

-- supplier_products table: Put this in a junction table rather than directly on the product. Multiple suppliers often sell the same product, and they might charge different unit_costs.

-- UUIDs: Used UUIDs for all primary keys to prevent ID enumeration and make data migrations/sharding easier for a SaaS platform.

-- Unique Constraints: Enforced uniqueness on (company_id, sku) so a business can't create duplicate SKUs, and (warehouse_id, product_id) so a warehouse doesn't have duplicate tracking rows for the same item.--