# order-management-system

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
        <a href="#about-the-project">About The Project</a>
    </li>
    <li>
        <a href="#built-with">Built With</a></li>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
        <ul>
            <li><a href="#prerequisites">Prerequisites</a></li>
            <li><a href="#installation">Installation</a></li>
        </ul>
    </li>
    <li>
        <a href="#usage">Usage</a>
        <ul>
            <li><a href="#running-api">Running API</a></li>
            <li><a href="#running-tests">Running Tests</a></li>
            <li><a href="#running-both">Running Both</a></li>
        </ul>
    </li>
    <li>
        <a href="#examples-of-using-the-api">Examples of using the API</a>
        <ul>
            <li><a href="#create-order">Create Order</a></li>
            <li><a href="#get-order-by-id">Get Order by ID</a></li>
            <li><a href="#get-all-orders">Get All Orders</a></li>
            <li><a href="#update-order">Update Order</a></li>
            <li><a href="#bulk-update-order-statuses">Bulk Update Order Statuses<a></li>
            <li><a href="#delete-order-by-id">Delete Order by ID</a></li>
            <li><a href="#get-order-statistics">Get Order Statistics</a></li>
            <li><a href="#generate-xlsx-report">Generate XLSX Report</a></li>
            <li><a href="#export-orders-to-xml">Export Orders to XML</a></li>
            <li><a href="#import-orders-from-xml">Import Orders from XML</a></li>
            <li><a href="#export-orders-to-hdf5">Export Orders to HDF5<a></li>
            <li><a href="#import-orders-from-hdf5">Import Orders from HDF5</a></li>
        </ul>
    </li>
    <li>
        <a href="#sample-files">Sample Files</a>
    </li>
  </ol>
</details>

## About The Project

Order Management System provides users with ability to create, update, view and delete orders. It supports generating XLSX reports and offers importing and exporting data using XML or HDF5 file formats.

## Built With

- ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## Getting Started

This section provides step-by-step instructions on how to set up the project locally.

### Prerequisites

Ensure you have Docker and Docker Compose installed on your local machine.

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/fsosn/order-management-system.git
   ```
2. Make sure Docker is running.
3. Navigate to project directory.
4. Build Docker containers:
   ```sh
   docker-compose build
   ```

## Usage

#### Running API

To start API and database:

```sh
docker-compose up api
```

The API will be accessible at `http://localhost:5000` after running this command.

#### Running Tests

To run tests using pytest and a separate test database:

```sh
docker-compose up tests
```

This command will build the necessary containers to automatically run prepared tests and display coverage report.

#### Running Both

To run both the API and the tests:

```sh
docker-compose up
```

## Examples of using the API

#### Create Order

```sh
curl -X POST http://localhost:5000/api/orders -H "Content-Type: application/json" -d '{
  "name": "New Order",
  "description": "This is a new order.",
  "status": "NEW"
}'
```

Status is optional when creating a new order, it is "NEW" by default. Allowed status values are: `NEW`, `IN_PROGRESS` and `COMPLETED`.

#### Get Order by ID

```sh
curl -X GET http://localhost:5000/api/orders/1
```

#### Get All Orders

```sh
curl -X GET http://localhost:5000/api/orders
```

#### Update Order

```sh
curl -X PUT http://localhost:5000/api/orders/1 -H "Content-Type: application/json" -d '{
  "name": "Updated Order",
  "description": "This is an updated order.",
  "status": "COMPLETED"
}'
```

#### Bulk Update Order Statuses

```sh
curl -X PUT http://localhost:5000/api/orders -H "Content-Type: application/json" -d '{
"id_list": [1, 2, 3],
"status": "COMPLETED"
}'
```

#### Delete Order by ID

```sh
curl -X DELETE http://localhost:5000/api/orders/1
```

#### Get Order Statistics

```sh
curl -X GET http://localhost:5000/api/orders/statistics
```

#### Generate XLSX Report

```sh
curl -X GET http://localhost:5000/api/orders/xlsx-report --output orders_report.xlsx
```

#### Export Orders to XML

```sh
curl -X GET http://localhost:5000/api/orders/export/xml --output orders.xml
```

#### Import Orders from XML

```sh
curl -X POST http://localhost:5000/api/orders/import/xml -F "file=@orders.xml"
```

#### Export Orders to HDF5

```sh
curl -X GET http://localhost:5000/api/orders/export/hdf5 --output orders.h5
```

#### Import Orders from HDF5

```sh
curl -X POST http://localhost:5000/api/orders/import/hdf5 -F "file=@orders.h5"
```

## Sample Files

Sample files of generated XLSX report and orders exported to XML and HDF5 are located in `/sample_files` directory.
