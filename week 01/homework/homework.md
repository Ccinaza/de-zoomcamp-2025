# Module 1 Homework: Docker & SQL

In this homework, we'll prepare the environment and practice Docker and SQL. 

## Questions and Answers

### Question 1: Understanding Docker First Run
Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.
What's the version of pip in the image?

**Options**:
- [ ] 24.3.1
- [ ] 24.2.1
- [ ] 23.3.1
- [ ] 23.2.1

**Answer**:  
The code to run Docker with this image of Python in interactive mode and by using `bash` is:

```bash
docker run -it --entrypoint=bash python:3.12.8
```
This command pulls the `Python 3.12.8` image, runs it in an interactive terminal `(-it)`, and overrides the default entrypoint with `bash`.

The output was:
```
Status: Downloaded newer image for python:3.12.8
```

To check the pip version, I ran the following command:

```bash
pip --version
```

The output was:

```
root@c6f17597d787:/# pip --version
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

### Question 2: Understanding Docker Networking and docker-compose

Given the following `docker-compose.yaml`, what is the hostname and port that pgAdmin should use to connect to the Postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

 **Options**:
  - `postgres:5433`
  - `localhost:5432`
  - `db:5433`
  - `postgres:5432`
  - `db:5432`

Docker Compose allows you to define and run multi-container Docker applications. Services within the same Docker Compose file are automatically part of the same network and can communicate using their service names.

The `ports` section maps the container's internal port to an external host port. For example, in the `db` service, `5433:5432 `means:

`5432` is the internal port of the Postgres container, where the database service listens for connections inside the Docker network.

`5433` is the port on your host machine (your laptop) that is mapped to the container's port `5432`, making the service accessible from outside Docker.

For `pgadmin` to connect to `Postgres` within the Docker network, the hostname will be `db` (the service name), and the port will be the internal port `5432`. Why? This is because in Docker Compose, services use their service names (e.g., db) to communicate, not container names (e.g., postgres).

**Answer**:  
The hostname and port that pgAdmin should use to connect to the Postgres database are:

```plaintext
db:5432
```

## Prepare Postgres
Run Postgres and load data as shown in the videos We'll use the green taxi trips from October 2019:

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
You will also need the dataset with zones:

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
Download this data and put it into Postgres.

To run the Postgres and pdadmin containers, I used the following command:
```bash
docker-compose up -d
```
To ingest data into Postgres, I used the following command:
```bash
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5434 \
  --db=ny_taxi \
  --taxi_table=green_taxi \
  --zones_table=zones \
  --taxi_url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz \
  --zones_url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```


## Question 3: Trip Segmentation Count

During the period of October 1st, 2019 (inclusive) and November 1st, 2019 (exclusive), how many trips, respectively, happened:

1. Up to 1 mile
2. Between 1 (exclusive) and 3 miles (inclusive)
3. Between 3 (exclusive) and 7 miles (inclusive)
4. Between 7 (exclusive) and 10 miles (inclusive)
5. Over 10 miles

**Options**:

- 104,802; 197,670; 110,612; 27,831; 35,281
- 104,802; 198,924; 109,603; 27,678; 35,189
- 104,793; 201,407; 110,612; 27,831; 35,281
- 104,793; 202,661; 109,603; 27,678; 35,189
- 104,838; 199,013; 109,645; 27,688; 35,202

**Answer**:  
To answer this question, the SQL query I used was:

```sql
select
    sum(case when trip_distance <= 1 then 1 else 0 end) as up_to_1_mile,
    sum(case when trip_distance > 1 and trip_distance <= 3 then 1 else 0 end) as between_1_to_3_miles,
    sum(case when trip_distance > 3 and trip_distance <= 7 then 1 else 0 end) as between_3_to_7_miles,
    sum(case when trip_distance > 7 and trip_distance <= 10 then 1 else 0 end) as between_7_to_10_miles,
    sum(case when trip_distance > 10 then 1 else 0 end) as Over_10_miles 
from 
    green_taxi
where 
    (date(lpep_pickup_datetime) >= '2019-10-01' 
    and date(lpep_dropoff_datetime) < '2019-11-01');
```

The output was:
```
+--------------+----------------------+----------------------+-----------------------+---------------+
| up_to_1_mile | between_1_to_3_miles | between_3_to_7_miles | between_7_to_10_miles | over_10_miles |
|--------------+----------------------+----------------------+-----------------------+---------------|
| 104802       | 198924               | 109603               | 27678                 | 35189         |
+--------------+----------------------+----------------------+-----------------------+---------------+
```

## Question 4: Longest Trip for Each Day

Which was the pick-up day with the longest trip distance? Use the pick-up time for your calculations.

**Answer**:  
SQL Query:

```sql
select 
    date(lpep_pickup_datetime) as pickup_time,
    max(trip_distance) as max_trip_distance
from 
    green_taxi
group by
    date(lpep_pickup_datetime)
order by 
    max_trip_distance desc
limit 1;
```

- The `GROUP BY DATE(lpep_pickup_datetime)` groups trips by each day, enabling the query to calculate the maximum trip distance `(MAX(trip_distance))` for every individual day.

- Without `GROUP BY`, the query would calculate the overall longest trip distance for the entire dataset instead of finding it for each specific day.

The output was:
```
+-------------+-------------------+
| pickup_time | max_trip_distance |
|-------------+-------------------|
| 2019-10-31  | 515.89            |
+-------------+-------------------+
```

## Question 5: Three Biggest Pickup Zones

Which were the top pickup locations with over 13,000 in total amount (across all trips) for 2019-10-18?
Consider only `lpep_pickup_datetime` when filtering by date.

 **Options**:
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

**Answer**:  
SQL:

```sql
select 
    z."Zone", 
    sum(g.total_amount) as total_amount
from 
    green_taxi g
inner join 
    zones z on g."PULocationID" = z."LocationID"
where 
    date(lpep_pickup_datetime) = '2019-10-18'
group by 1
having 
    sum(g.total_amount) > 13000
order by 
    total_amount desc
```

The output was:
```
+---------------------+--------------------+
| Zone                | total_amount       |
|---------------------+--------------------|
| East Harlem North   | 18686.68000000003  |
| East Harlem South   | 16797.26000000006  |
| Morningside Heights | 13029.790000000035 |
+---------------------+--------------------+
```

## Question 6: Largest Tip

For passengers picked up in October 2019 in the zone name "East Harlem North," which was the drop-off zone that had the largest tip?

Note: it's tip , not trip

We need the name of the zone, not the ID.

 **Options**:
- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South

**Answer**:  
SQL:

```sql
select 
    zd."Zone" as dropoff_zone,
	max(g.tip_amount) AS largest_tip
from 
    green_taxi g
left join 
    zones z on g."PULocationID" = z."LocationID"
left join 
    zones zd ON g."DOLocationID" = zd."LocationID"
where z."Zone" = 'East Harlem North'
    and date(g.lpep_pickup_datetime) between '2019-10-01' and '2019-10-31' 
group by
    zd."Zone"
order by 
    largest_tip desc
limit 1;
```

The output was:
```
+--------------+-------------+
| dropoff_zone | largest_tip |
|--------------+-------------|
| JFK Airport  | 87.3        |
+--------------+-------------+
```

## Question 7: Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up backend
2. Generating proposed changes and auto-executing the plan
3. Removing all resources managed by Terraform

**Options**:

- `terraform import, terraform apply -y, terraform destroy`
- `terraform init, terraform plan -auto-apply, terraform rm`
- `terraform init, terraform run -auto-approve, terraform destroy`
- `terraform init, terraform apply -auto-approve, terraform destroy`
- `terraform import, terraform apply -y, terraform rm`

**The correct answer is:**
`terraform init, terraform apply -auto-approve, terraform destroy`

Explanation:
To download provider plugins and set up the backend, you will need to run this command:
```bash
Command: terraform init
```
This initializes the Terraform configuration, downloads the provider plugins, and sets up the backend for storing the state.

To generate proposed changes and auto-execute the plan, you will need to run this command:
```bash
Command: terraform apply -auto-approve
```
This applies the changes in the Terraform plan and auto-approves without requiring manual confirmation.

To remove all resources managed by Terraform, you will need to run this command:
```bash
Command: terraform destroy
```
This destroys all resources that Terraform manages in the current state.