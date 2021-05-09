--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

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
-- Name: uuid(); Type: FUNCTION; Schema: public; Owner: qfinder_user
--

CREATE FUNCTION public.uuid() RETURNS uuid
    LANGUAGE sql
    AS $$SELECT uuid_in(md5(random()::text)::cstring)$$;


ALTER FUNCTION public.uuid() OWNER TO qfinder_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admins; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.admins (
    id uuid DEFAULT public.uuid() NOT NULL,
    active boolean,
    confirmed_at timestamp without time zone,
    password text NOT NULL,
    email text NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.admins OWNER TO qfinder_user;

--
-- Name: admins_to_roles; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.admins_to_roles (
    admin_id uuid NOT NULL,
    role_id uuid NOT NULL
);


ALTER TABLE public.admins_to_roles OWNER TO qfinder_user;

--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.cart_items (
    id uuid DEFAULT public.uuid() NOT NULL,
    user_id uuid NOT NULL,
    product_id uuid NOT NULL
);


ALTER TABLE public.cart_items OWNER TO qfinder_user;

--
-- Name: feedback; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.feedback (
    id uuid DEFAULT public.uuid() NOT NULL,
    user_id uuid NOT NULL,
    product_id uuid NOT NULL,
    body text NOT NULL,
    stars smallint NOT NULL,
    CONSTRAINT feedback_stars_check CHECK (((stars <= 5) AND (stars >= 0)))
);


ALTER TABLE public.feedback OWNER TO qfinder_user;

--
-- Name: product_pictures; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.product_pictures (
    id uuid DEFAULT public.uuid() NOT NULL,
    product_id uuid NOT NULL,
    link text NOT NULL
);


ALTER TABLE public.product_pictures OWNER TO qfinder_user;

--
-- Name: product_types; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.product_types (
    id uuid DEFAULT public.uuid() NOT NULL,
    name text NOT NULL,
    picture text NOT NULL
);


ALTER TABLE public.product_types OWNER TO qfinder_user;

--
-- Name: products; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.products (
    id uuid DEFAULT public.uuid() NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    characteristics json NOT NULL,
    type uuid NOT NULL,
    price integer NOT NULL
);


ALTER TABLE public.products OWNER TO qfinder_user;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.roles (
    id uuid DEFAULT public.uuid() NOT NULL,
    name text NOT NULL,
    description text
);


ALTER TABLE public.roles OWNER TO qfinder_user;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.tags (
    id uuid DEFAULT public.uuid() NOT NULL,
    title text NOT NULL
);


ALTER TABLE public.tags OWNER TO qfinder_user;

--
-- Name: tags_to_products; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.tags_to_products (
    id uuid DEFAULT public.uuid() NOT NULL,
    product_id uuid NOT NULL,
    tag_id uuid NOT NULL
);


ALTER TABLE public.tags_to_products OWNER TO qfinder_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.users (
    id uuid DEFAULT public.uuid() NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    first_name text,
    last_name text
);


ALTER TABLE public.users OWNER TO qfinder_user;

--
-- Name: wishlist; Type: TABLE; Schema: public; Owner: qfinder_user
--

CREATE TABLE public.wishlist (
    id uuid DEFAULT public.uuid() NOT NULL,
    user_id uuid NOT NULL,
    product_id uuid NOT NULL
);


ALTER TABLE public.wishlist OWNER TO qfinder_user;

--
-- Name: admins admins_email_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_email_key UNIQUE (email);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: cart_items cart_items_user_id_product_id_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_user_id_product_id_key UNIQUE (user_id, product_id);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- Name: product_pictures product_pictures_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.product_pictures
    ADD CONSTRAINT product_pictures_pkey PRIMARY KEY (id);


--
-- Name: products products_name_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_name_key UNIQUE (name);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: product_types products_types_name_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.product_types
    ADD CONSTRAINT products_types_name_key UNIQUE (name);


--
-- Name: product_types products_types_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.product_types
    ADD CONSTRAINT products_types_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: tags tags_title_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_title_key UNIQUE (title);


--
-- Name: tags_to_products tags_to_products_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.tags_to_products
    ADD CONSTRAINT tags_to_products_pkey PRIMARY KEY (id);


--
-- Name: tags_to_products tags_to_products_product_id_tag_id_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.tags_to_products
    ADD CONSTRAINT tags_to_products_product_id_tag_id_key UNIQUE (product_id, tag_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: wishlist wishlist_pkey; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT wishlist_pkey PRIMARY KEY (id);


--
-- Name: wishlist wishlist_user_id_product_id_key; Type: CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT wishlist_user_id_product_id_key UNIQUE (user_id, product_id);


--
-- Name: admins_to_roles admins_to_roles_admin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.admins_to_roles
    ADD CONSTRAINT admins_to_roles_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public.admins(id) ON DELETE CASCADE;


--
-- Name: admins_to_roles admins_to_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.admins_to_roles
    ADD CONSTRAINT admins_to_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: cart_items cart_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: cart_items cart_items_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: feedback feedback_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: feedback feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: product_pictures product_pictures_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.product_pictures
    ADD CONSTRAINT product_pictures_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: products products_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_type_fkey FOREIGN KEY (type) REFERENCES public.product_types(id);


--
-- Name: tags_to_products tags_to_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.tags_to_products
    ADD CONSTRAINT tags_to_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: tags_to_products tags_to_products_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.tags_to_products
    ADD CONSTRAINT tags_to_products_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- Name: wishlist wishlist_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT wishlist_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: wishlist wishlist_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qfinder_user
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT wishlist_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

