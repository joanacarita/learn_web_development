CREATE TABLE public.medicos (
	id serial4 NOT NULL,
	nome text NOT NULL,
	apelido text NOT NULL,
	numero_ordem text NOT NULL,
	email text NOT NULL,
	"password" text NOT NULL,
	local_trabalho text NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT utilizadores_pkey PRIMARY KEY (id)
);