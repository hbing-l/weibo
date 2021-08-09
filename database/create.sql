--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

-- Started on 2021-08-09 19:10:32 CST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 3079 OID 24714)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3371 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- TOC entry 2 (class 3079 OID 24677)
-- Name: pldbgapi; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pldbgapi WITH SCHEMA public;


--
-- TOC entry 3372 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pldbgapi; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pldbgapi IS 'server-side support for debugging PL/pgSQL functions';


--
-- TOC entry 281 (class 1255 OID 24756)
-- Name: auto_add_comment(); Type: FUNCTION; Schema: public; Owner: user1
--

CREATE FUNCTION public.auto_add_comment() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
     update public.message set comment_count=comment_count+1 where id = NEW.message_id;
     RETURN NEW;
END;
$$;


ALTER FUNCTION public.auto_add_comment() OWNER TO user1;

--
-- TOC entry 280 (class 1255 OID 24751)
-- Name: calculate_cnt(); Type: PROCEDURE; Schema: public; Owner: user1
--

CREATE PROCEDURE public.calculate_cnt()
    LANGUAGE plpgsql
    AS $$
DECLARE
	comment_cnt bigint;
	
BEGIN
	
	FOR i in 1..100000 LOOP
		SELECT COUNT(*) FROM public.comment WHERE message_id=i into comment_cnt;
		UPDATE "message" SET comment_count=comment_cnt WHERE id=i;
	END LOOP;
	
END;
$$;


ALTER PROCEDURE public.calculate_cnt() OWNER TO user1;

--
-- TOC entry 279 (class 1255 OID 24676)
-- Name: create_message(); Type: PROCEDURE; Schema: public; Owner: user1
--

CREATE PROCEDURE public.create_message()
    LANGUAGE plpgsql
    AS $$
DECLARE 
num bigint;
per_num bigint;

BEGIN
	
	SELECT 1 into num;
	SELECT 0 into per_num;

	FOR i IN 1..100000 LOOP
		INSERT INTO "message" ("id", "content",comment_count) VALUES (i, 'message',0);
		SELECT floor(random()*(10-1)+10)::bigint into per_num;
		UPDATE "message" SET comment_count=per_num where id=i;
		FOR j IN num..(num+per_num) LOOP
			INSERT INTO "comment" ("id", message_id, "content") VALUES (j, i, 'comment');
		END LOOP;
		SELECT (num+per_num+1)::bigint into num;
	END LOOP;
		
END;
$$;


ALTER PROCEDURE public.create_message() OWNER TO user1;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 24651)
-- Name: comment; Type: TABLE; Schema: public; Owner: user1
--

CREATE TABLE public.comment (
    id bigint NOT NULL,
    message_id bigint,
    content character varying(255),
    comment_date time with time zone
);


ALTER TABLE public.comment OWNER TO user1;

--
-- TOC entry 205 (class 1259 OID 24661)
-- Name: follow; Type: TABLE; Schema: public; Owner: user1
--

CREATE TABLE public.follow (
    id bigint NOT NULL,
    user_id bigint,
    follow_id bigint,
    follow_date time with time zone
);


ALTER TABLE public.follow OWNER TO user1;

--
-- TOC entry 203 (class 1259 OID 24638)
-- Name: message; Type: TABLE; Schema: public; Owner: user1
--

CREATE TABLE public.message (
    id bigint NOT NULL,
    user_id bigint,
    content character varying(255),
    link character varying(255),
    send_date time with time zone,
    comment_count bigint
);


ALTER TABLE public.message OWNER TO user1;

--
-- TOC entry 202 (class 1259 OID 24624)
-- Name: user; Type: TABLE; Schema: public; Owner: user1
--

CREATE TABLE public."user" (
    id bigint NOT NULL,
    password character varying(255),
    email character varying(255),
    name character varying(255),
    activation_link character varying(255),
    is_activated boolean,
    reset_password_link character varying(255),
    send_reset_link_date time with time zone,
    is_deleted boolean
);


ALTER TABLE public."user" OWNER TO user1;

--
-- TOC entry 3364 (class 0 OID 24651)
-- Dependencies: 204
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: user1
--

--
-- TOC entry 3221 (class 2606 OID 24655)
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (id);


--
-- TOC entry 3225 (class 2606 OID 24665)
-- Name: follow follow_pkey; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.follow
    ADD CONSTRAINT follow_pkey PRIMARY KEY (id);


--
-- TOC entry 3218 (class 2606 OID 24645)
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- TOC entry 3210 (class 2606 OID 24635)
-- Name: user user_activation_link_key; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_activation_link_key UNIQUE (activation_link);


--
-- TOC entry 3212 (class 2606 OID 24633)
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- TOC entry 3214 (class 2606 OID 24631)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3216 (class 2606 OID 24637)
-- Name: user user_reset_password_link_key; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_reset_password_link_key UNIQUE (reset_password_link);


--
-- TOC entry 3223 (class 1259 OID 24754)
-- Name: follow_id_index; Type: INDEX; Schema: public; Owner: user1
--

CREATE INDEX follow_id_index ON public.follow USING btree (follow_id);


--
-- TOC entry 3226 (class 1259 OID 24753)
-- Name: follow_user_id_index; Type: INDEX; Schema: public; Owner: user1
--

CREATE INDEX follow_user_id_index ON public.follow USING btree (user_id);


--
-- TOC entry 3222 (class 1259 OID 24755)
-- Name: message_id_index; Type: INDEX; Schema: public; Owner: user1
--

CREATE INDEX message_id_index ON public.comment USING btree (message_id);


--
-- TOC entry 3219 (class 1259 OID 24752)
-- Name: user_id_index; Type: INDEX; Schema: public; Owner: user1
--

CREATE INDEX user_id_index ON public.message USING btree (user_id);


--
-- TOC entry 3231 (class 2620 OID 24757)
-- Name: comment auto_add_trigger; Type: TRIGGER; Schema: public; Owner: user1
--

CREATE TRIGGER auto_add_trigger BEFORE INSERT ON public.comment FOR EACH ROW EXECUTE FUNCTION public.auto_add_comment();


--
-- TOC entry 3228 (class 2606 OID 24656)
-- Name: comment comment_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.message(id);


--
-- TOC entry 3230 (class 2606 OID 24671)
-- Name: follow follow_follow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.follow
    ADD CONSTRAINT follow_follow_id_fkey FOREIGN KEY (follow_id) REFERENCES public."user"(id);


--
-- TOC entry 3229 (class 2606 OID 24666)
-- Name: follow follow_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.follow
    ADD CONSTRAINT follow_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- TOC entry 3227 (class 2606 OID 24646)
-- Name: message message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


-- Completed on 2021-08-09 19:10:32 CST

--
-- PostgreSQL database dump complete
--

