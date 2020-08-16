-- DROP SCHEMA main;

CREATE SCHEMA main AUTHORIZATION cloudsqlsuperuser;

-- main.customer definition

-- Drop table

-- DROP TABLE main.customer;

CREATE TABLE main.customer (
	id serial NOT NULL,
	mail varchar(200) NULL,
	full_name varchar(200) NULL,
	cellphone varchar(200) NULL,
	photo varchar(400) NULL,
	"password" varchar(400) NULL,
	status int4 NULL,
	CONSTRAINT customer_pkey PRIMARY KEY (id)
);

-- main.customer_address definition

-- Drop table

-- DROP TABLE main.customer_address;

CREATE TABLE main.customer_address (
	id serial NOT NULL,
	id_customer int4 NULL,
	address varchar(500) NULL,
	longitude varchar(100) NULL,
	latitude varchar(100) NULL,
	main int4 NULL,
	status int4 NULL,
	CONSTRAINT customer_address_pkey PRIMARY KEY (id)
);

-- main.customer_card definition

-- Drop table

-- DROP TABLE main.customer_card;

CREATE TABLE main.customer_card (
	id serial NOT NULL,
	id_customer int4 NULL,
	id_type_card int4 NULL,
	document_number varchar(100) NULL,
	expiration_year varchar(10) NULL,
	expiration_month varchar(10) NULL,
	email varchar(300) NULL,
	status int4 NULL,
	CONSTRAINT customer_card_pkey PRIMARY KEY (id)
);

-- main.customer_rate definition

-- Drop table

-- DROP TABLE main.customer_rate;

CREATE TABLE main.customer_rate (
	id_user int4 NULL,
	id_service int4 NULL,
	id_customer int4 NULL,
	rate int4 NULL,
	description varchar(300) NULL,
	status int4 NULL
);

-- main.hour_availability definition

-- Drop table

-- DROP TABLE main.hour_availability;

CREATE TABLE main.hour_availability (
	hour_availability int4 NOT NULL,
	status int4 NULL,
	CONSTRAINT hour_availability_pkey PRIMARY KEY (hour_availability)
);

-- main.sale definition

-- Drop table

-- DROP TABLE main.sale;

CREATE TABLE main.sale (
	id serial NOT NULL,
	id_type_availability int4 NULL,
	id_customer int4 NULL,
	id_user int4 NULL,
	coupon varchar(300) NULL,
	date_availability date NULL,
	hour_availability int4 NULL,
	total_amount float8 NULL,
	id_card int4 NULL,
	status int4 NULL,
	CONSTRAINT sale_pkey PRIMARY KEY (id)
);

-- main.service definition

-- Drop table

-- DROP TABLE main.service;

CREATE TABLE main.service (
	id serial NOT NULL,
	full_name varchar(200) NULL,
	url_image varchar(300) NULL,
	status int4 NULL,
	color varchar(50) NULL,
	CONSTRAINT service_pkey PRIMARY KEY (id)
);

-- main.sub_service definition

-- Drop table

-- DROP TABLE main.sub_service;

CREATE TABLE main.sub_service (
	id serial NOT NULL,
	id_service int4 NULL,
	full_name varchar(200) NULL,
	status int4 NULL,
	CONSTRAINT sub_service_pkey PRIMARY KEY (id)
);

-- main.type_availability definition

-- Drop table

-- DROP TABLE main.type_availability;

CREATE TABLE main.type_availability (
	id serial NOT NULL,
	full_name varchar(100) NULL,
	status int4 NULL,
	CONSTRAINT type_availability_pkey PRIMARY KEY (id)
);

-- main.type_card definition

-- Drop table

-- DROP TABLE main.type_card;

CREATE TABLE main.type_card (
	id serial NOT NULL,
	brand varchar(200) NULL,
	url_image varchar(300) NULL,
	status int4 NULL,
	CONSTRAINT type_card_pkey PRIMARY KEY (id)
);

-- main.type_document definition

-- Drop table

-- DROP TABLE main.type_document;

CREATE TABLE main.type_document (
	id serial NOT NULL,
	full_name varchar(100) NULL,
	status int4 NULL,
	CONSTRAINT type_document_pkey PRIMARY KEY (id)
);

-- main.type_sale definition

-- Drop table

-- DROP TABLE main.type_sale;

CREATE TABLE main.type_sale (
	id serial NOT NULL,
	id_sale int4 NULL,
	id_sub_service int4 NULL,
	amount float8 NULL,
	status int4 NULL,
	CONSTRAINT type_sale_pkey PRIMARY KEY (id)
);

-- main.user_date_availability definition

-- Drop table

-- DROP TABLE main.user_date_availability;

CREATE TABLE main.user_date_availability (
	id_user int4 NULL,
	id_type_availability int4 NULL,
	date_availability date NULL,
	hour_availability int4 NULL,
	"enable" int4 NULL,
	status int4 NULL
);

-- main.user_p definition

-- Drop table

-- DROP TABLE main.user_p;

CREATE TABLE main.user_p (
	id serial NOT NULL,
	mail varchar(100) NULL,
	social_name varchar(200) NULL,
	full_name varchar(300) NULL,
	document_number varchar(100) NULL,
	type_user varchar(50) NULL,
	photo varchar(100) NULL,
	status int4 NULL,
	"password" varchar(400) NULL,
	cellphone varchar(50) NULL,
	about varchar(5000) NULL,
	id_type_document int4 NULL,
	CONSTRAINT user_p_pkey PRIMARY KEY (id)
);

-- main.user_push definition

-- Drop table

-- DROP TABLE main.user_push;

CREATE TABLE main.user_push (
	id_user int4 NULL,
	push_code varchar(5000) NULL,
	status int4 NULL
);

-- main.user_service definition

-- Drop table

-- DROP TABLE main.user_service;

CREATE TABLE main.user_service (
	id_user int4 NULL,
	id_service int4 NULL,
	status int4 NULL,
	"enable" int4 NULL
);

-- main.user_store definition

-- Drop table

-- DROP TABLE main.user_store;

CREATE TABLE main.user_store (
	id serial NOT NULL,
	id_user int4 NULL,
	full_name varchar(500) NULL,
	address varchar(500) NULL,
	longitude varchar(100) NULL,
	latitude varchar(100) NULL,
	main int4 NULL,
	status int4 NULL,
	CONSTRAINT user_store_pkey PRIMARY KEY (id)
);

-- main.user_sub_service definition

-- Drop table

-- DROP TABLE main.user_sub_service;

CREATE TABLE main.user_sub_service (
	id_user int4 NULL,
	id_service int4 NULL,
	id_sub_service int4 NULL,
	charge float8 NULL,
	"enable" int4 NULL,
	status int4 NULL
);