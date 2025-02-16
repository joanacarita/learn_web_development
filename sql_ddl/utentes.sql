-- public.utentes definition

-- Drop table

-- DROP TABLE public.utentes;

CREATE TABLE public.utentes (
	id serial4 NOT NULL,
	medico_id int4 NOT NULL,
	nome text NOT NULL,
	apelido text NOT NULL,
	numero_utente text NOT NULL,
	email text NOT NULL,
	data_nascimento date NOT NULL,
	sexo text NULL,
	peso int4 NULL,
	altura int4 NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT utentes_pkey PRIMARY KEY (id)
);