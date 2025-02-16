    -- public.quest_respostas definition

-- Drop table

-- DROP TABLE public.quest_respostas;

CREATE TABLE public.quest_respostas (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	quest_nome text NOT NULL,
	num_pergunta int4 NOT NULL,
	valor_resposta int4 NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT quest_respostas_pkey PRIMARY KEY (id)
);