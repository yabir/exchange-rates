create schema operations;

create table operations.station (
	station_id serial primary key,
	name varchar(50),
	geolocation point,
	street varchar(50),
	number int,
	city varchar(50),
	country varchar(50),
	created_on timestamp default now(),
	last_updated_on timestamp
);

comment on table operations.station is 'Table of bus stations';
comment on column operations.station.station_id is 'Station identification number';
comment on column operations.station.name is 'Station name';
comment on column operations.station.geolocation is 'Station location latitude and longitude';
comment on column operations.station.street is 'Station street name';
comment on column operations.station.number is 'Station address number';
comment on column operations.station.city is 'Station city';
comment on column operations.station.country is 'Station Country';

create table operations.category (
	category_id serial primary key,
	name varchar(50) not null,
	created_on timestamp default now(),
	last_updated_on timestamp
);

comment on table operations.category is 'Table of category of additional products. Ex : movies, assurance, seats.';
comment on column operations.category.category_id is 'Category identification number';
comment on column operations.category.name is 'Category name';

create table operations.additional_products (
	additional_product_id serial primary key,
	category_id int not null,
	name varchar(50) not null,
	short_description varchar(25) not null,
	long_description varchar(500) not null,
	price float not null,
	created_on timestamp default now(),
	last_updated_on timestamp,
	FOREIGN KEY (category_id) REFERENCES operations.category (category_id)
);

comment on table operations.additional_products is 'Table of additional products';
comment on column operations.additional_products.additional_product_id is 'Additional Product identification number';
comment on column operations.additional_products.category_id is '[FK] Table -> category';
comment on column operations.additional_products.name is 'Additional Product name';
comment on column operations.additional_products.short_description is 'Additional Product short description for websites and mobile apps';
comment on column operations.additional_products.long_description is 'Additional Product long description for Product''s profile page in websites and mobiles apps';
comment on column operations.additional_products.price is 'Additional Product price';

create table operations.passenger (
	passenger_id serial primary key,
	name varchar(50),
	lastname varchar(50),
	birthday date,
	is_affiliated boolean,
	email varchar(50),
	crypt_password varchar(50),
	created_on timestamp default now(),
	last_updated_on timestamp
);

comment on table operations.passenger is 'Table of passengers. Note : not all the users have an account in platform';
comment on column operations.passenger.passenger_id is 'Passenger identification number';
comment on column operations.passenger.name is 'Passenger name';
comment on column operations.passenger.lastname is 'Passenger lastname';
comment on column operations.passenger.birthday is 'Passenger date of birth';
comment on column operations.passenger.is_affiliated is 'Flag of passenger''s statut of in platform. If true, this passenger has an account in the platform';
comment on column operations.passenger.email is 'Passenger email';
comment on column operations.passenger.crypt_password is 'Passenger encrypted password. Algorithm : ...';

create table operations.booking (
	booking_id serial primary key,
	qty_passengers int not null,
	buyer_passenger_id int not null,
	total_price float not null,
	purchased_date timestamp not null,
	FOREIGN KEY (buyer_passenger_id) REFERENCES operations.passenger (passenger_id)
);

comment on table operations.booking is 'Table of Bookings';
comment on column operations.booking.booking_id is 'Booking identification number';
comment on column operations.booking.qty_passengers is 'Quantity of passengers in booking';
comment on column operations.booking.buyer_passenger_id is '[FK] Table -> passenger. Passenger that made the booking';
comment on column operations.booking.total_price is 'Booking total price';

create table operations.booking_additional_product (
	booking_id int not null,
	additional_product_id int not null,
	FOREIGN KEY (additional_product_id) REFERENCES operations.additional_products (additional_product_id),
	FOREIGN KEY (booking_id) REFERENCES operations.booking (booking_id)
);

comment on table operations.booking_additional_product is 'Relational table of tables : booking and addition_product';
comment on column operations.booking_additional_product.booking_id is '[FK] Table -> booking.';
comment on column operations.booking_additional_product.additional_product_id is '[FK] Table -> additional_product.';

create table operations.driver (
	driver_id serial primary key,
	name varchar(50),
	lastname varchar(50),
	created_on timestamp default now(),
	last_updated_on timestamp
);

comment on table operations.driver is 'Table of Drivers';
comment on column operations.driver.driver_id is 'Driver identification number';
comment on column operations.driver.name is 'Driver name.';
comment on column operations.driver.lastname is 'Driver lastname.';

create table operations.od (
	od_id serial primary key,
	origin_station_id int not null,
	destination_station_id int not null,
	price float not null,
	FOREIGN KEY (origin_station_id) REFERENCES operations.station (station_id),
	FOREIGN KEY (destination_station_id) REFERENCES operations.station (station_id)
);

comment on table operations.od is 'Table of Origin-Destinations (OD)';
comment on column operations.od.od_id is 'OD identification number';
comment on column operations.od.origin_station_id is 'Starting station of OD ';
comment on column operations.od.destination_station_id is 'Ending station of OD';
comment on column operations.od.price is 'Price of OD';

create table operations.ticket (
	booking_id int not null,
	od_id int not null,
	passenger_id int not null,
	FOREIGN KEY (booking_id) REFERENCES operations.booking (booking_id),
	FOREIGN KEY (od_id) REFERENCES operations.od (od_id),
	FOREIGN KEY (passenger_id) REFERENCES operations.passenger (passenger_id)	
);

comment on table operations.ticket is 'Table of Tickets : a Ticket should be stocked by every passenger in booking';
comment on column operations.ticket.booking_id is '[FK] Table -> booking. Booking of the OD';
comment on column operations.ticket.od_id is '[FK] Table -> od. Origin-Destination of the ticket ';
comment on column operations.ticket.passenger_id is '[FK] Table -> passenger. Passenger of the ticket';

create table operations.circulation (
	circulation_id serial primary key,		
	from_station_id int not null,
	to_station_id int not null,
	driver_id int not null,
	departure_time timestamp default now(),
	FOREIGN KEY (driver_id) REFERENCES operations.driver (driver_id),
	FOREIGN KEY (from_station_id) REFERENCES operations.station (station_id),
	FOREIGN KEY (to_station_id) REFERENCES operations.station (station_id)
);

comment on table operations.circulation is 'Table of Circulations: Stores all the stops the bus does';
comment on column operations.circulation.circulation_id is 'Circulation identification number';
comment on column operations.circulation.from_station_id is '[FK] Table -> station. Bus departure station ';
comment on column operations.circulation.to_station_id is '[FK] Table -> station. Bus ending station';
comment on column operations.circulation.driver_id is '[FK] Table -> driver. Driver of the journey';
comment on column operations.circulation.departure_time is 'Departure time of this journey';

create table operations.od_circulation (
	od_id int not null,
	circulation_id int not null,
	FOREIGN KEY (od_id) REFERENCES operations.od (od_id),
	FOREIGN KEY (circulation_id) REFERENCES operations.circulation (circulation_id)
);

comment on table operations.od_circulation is 'Relational table of tables : od and circulations';
comment on column operations.od_circulation.od_id is '[FK] Table -> od.';
comment on column operations.od_circulation.circulation_id is '[FK] Table -> circulation.';

create table operations.circulation_station (
	circulation_id int not null,
	station_id int not null,
	FOREIGN KEY (circulation_id) REFERENCES operations.circulation (circulation_id),
	FOREIGN KEY (station_id) REFERENCES operations.station (station_id)
);

comment on table operations.circulation_station is 'Relational table of tables : circulation and station';
comment on column operations.circulation_station.circulation_id is '[FK] Table -> circulation.';
comment on column operations.circulation_station.station_id is '[FK] Table -> station.';

-- Inventory
/*
select 
	s_origin.name as origin_station,
	s_destination.name as destination_station,
	c.departure_time,
	od.price,
	('Bus from: ' || s_origin.name || ' to ' || s_destination.name || ' at ' || c.departure_time || '. Price: ' || od.price) as message_example
from bus_network.od as od 
	inner join bus_network.station s_origin on od.origin_station_id = s_origin.station_id
	inner join bus_network.station s_destination on od.origin_station_id = s_destination.station_id
	inner join bus_network.od_circulation odc on od.od_id = odc.od_id
	inner join bus_network.circulation c on odc.circulation_id = c.circulation_id
where c.departure_time > now()
order by c.departure_time
*/

create schema analysis;

create table analysis.dim_driver (
	DriverKey int primary key,
	Name varchar(50) not null,
	Lastname varchar(50),
	Antiquity float
);

create table analysis.dim_passenger (
	PassengerKey int primary key,
	Name varchar(50) not null,
	LastName varchar(50) not null,
	Email varchar(100) not null,
	Age int,
	AffiliationIndicator boolean
);

create table analysis.dim_station (
	StationKey int primary key,
	Name varchar(50) not null,
	Geolocation_latitude float,
	Geolocation_longitude float,
	City varchar(100),
	Country varchar(100),
	CountryCode varchar(3)	
);

create table analysis.dim_departureTime (
	DepartureTimeKey date primary key,
	Day int not null,
	DayofWeek varchar(10) not null,
	Month int not null,
	Year int not null,
	HolidayIndicator boolean,
	WeekdayIndicator boolean,
	LeapYearIndicator boolean
);

create table analysis.fact_inventory (
	DepartureTimeKey date not null,
	FromStationKey int not null,
	ToStationKey int not null,
	PassengerKey int not null,
	DriverKey int not null,
	Price float not null,
	FOREIGN KEY (DepartureTimeKey) REFERENCES analysis.dim_departureTime (DepartureTimeKey),
	FOREIGN KEY (FromStationKey) REFERENCES analysis.dim_station (StationKey),
	FOREIGN KEY (ToStationKey) REFERENCES analysis.dim_station (StationKey),
	FOREIGN KEY (PassengerKey) REFERENCES analysis.dim_passenger (PassengerKey),
	FOREIGN KEY (DriverKey) REFERENCES analysis.dim_driver (DriverKey)
);







