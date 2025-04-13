--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-12 13:01:47

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 16665)
-- Name: client_configs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client_configs (
    id integer NOT NULL,
    user_id integer,
    location character varying,
    private_key character varying,
    public_key character varying,
    config_data character varying,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.client_configs OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16664)
-- Name: client_configs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_configs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_configs_id_seq OWNER TO postgres;

--
-- TOC entry 4925 (class 0 OID 0)
-- Dependencies: 221
-- Name: client_configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_configs_id_seq OWNED BY public.client_configs.id;


--
-- TOC entry 218 (class 1259 OID 16622)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16621)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4926 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 220 (class 1259 OID 16650)
-- Name: wireguard_configs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wireguard_configs (
    id integer NOT NULL,
    user_id integer,
    location character varying,
    private_key character varying,
    public_key character varying,
    config_data character varying
);


ALTER TABLE public.wireguard_configs OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16649)
-- Name: wireguard_configs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.wireguard_configs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.wireguard_configs_id_seq OWNER TO postgres;

--
-- TOC entry 4927 (class 0 OID 0)
-- Dependencies: 219
-- Name: wireguard_configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.wireguard_configs_id_seq OWNED BY public.wireguard_configs.id;


--
-- TOC entry 4755 (class 2604 OID 16668)
-- Name: client_configs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_configs ALTER COLUMN id SET DEFAULT nextval('public.client_configs_id_seq'::regclass);


--
-- TOC entry 4752 (class 2604 OID 16625)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4754 (class 2604 OID 16653)
-- Name: wireguard_configs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wireguard_configs ALTER COLUMN id SET DEFAULT nextval('public.wireguard_configs_id_seq'::regclass);


--
-- TOC entry 4919 (class 0 OID 16665)
-- Dependencies: 222
-- Data for Name: client_configs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client_configs (id, user_id, location, private_key, public_key, config_data, created_at) FROM stdin;
1	6	sweden	xeBOUi+3IzYisrUD043lC9p1sv1Llq48XqfXn8oJjnY=	ToAoCLfundOgU6F7DWh8mNMnl/AL+NvFzzxgGSM3mGA=	[Interface]\nPrivateKey = xeBOUi+3IzYisrUD043lC9p1sv1Llq48XqfXn8oJjnY=\nAddress = 10.0.0.2/32\nDNS = 8.8.8.8, 8.8.4.4\n\n[Peer]\nPublicKey = lagHVCshn3TLoxIANoXHGwdqXGmqE3dAww1A3Uyigxs=\nAllowedIPs = 0.0.0.0/0\nEndpoint = 51.21.167.201:51820\nPersistentKeepalive = 25\n	2025-04-11 17:36:14.917097
2	15	sweden	pJcCYtFxWXTtlFlHBH4JqoSMlIyhMI6AIyLpwqt5StM=	qHhJaQe7l0e1OZpHNOl080FLQOhZ5Fkyr6E3CVQf6ns=	[Interface]\nPrivateKey = pJcCYtFxWXTtlFlHBH4JqoSMlIyhMI6AIyLpwqt5StM=\nAddress = 10.0.0.2/32\nDNS = 8.8.8.8, 8.8.4.4\n\n[Peer]\nPublicKey = lagHVCshn3TLoxIANoXHGwdqXGmqE3dAww1A3Uyigxs=\nAllowedIPs = 0.0.0.0/0\nEndpoint = 51.21.167.201:51820\nPersistentKeepalive = 25\n	2025-04-11 21:47:01.671857
\.


--
-- TOC entry 4915 (class 0 OID 16622)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, created_at) FROM stdin;
1	aleksandr	ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f	2025-03-23 13:47:40.268542
2	jakub123	807ae5f38db47bff8b09b37ad803cb10ef5147567a89a33a66bb3282df4ad966	2025-03-23 13:59:56.238049
3	useruser	ee79976c9380d5e337fc1c095ece8c8f22f91f306ceeb161fa51fecede2c4ba1	2025-03-23 14:01:14.117117
4	new_user	29269867edc33eac60d69a7c82bffe40ea957e7dd5b737037534f8a3f35067c0	2025-03-23 14:08:26.390712
5	dfsafsdfasf	2413fb3709b05939f04cf2e92f7d0897fc2596f9ad0b8a9ea855c7bfebaae892	2025-03-25 19:55:24.706307
6	krakasevich	12697bbe5e5d14fda780af6390ae01ba0eece0839ece3f25b14671731b4d9a20	2025-03-25 20:10:10.352228
7	deniz	f0f01a1beaf798de0aee490e9110469fd3e1df5a627c5588659e6350579ba6a1	2025-03-26 20:56:23.169151
8	wqeqe	ed02457b5c41d964dbd2f2a609d63fe1bb7528dbe55e1abf5b52c249cd735797	2025-03-27 18:12:32.080526
9	TEST_USER	ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f	2025-03-27 18:18:28.819279
10	test_user	ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f	2025-03-27 18:26:48.629187
11	test_user1	ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f	2025-03-27 18:27:19.038773
12	aaaaaa	ed02457b5c41d964dbd2f2a609d63fe1bb7528dbe55e1abf5b52c249cd735797	2025-03-29 14:43:13.052004
13	alesha	bc4a09acd4c6a1e7389ef8f51958e6e817075db5c8c295a1024ab17d4dc57b1a	2025-04-02 02:07:36.995387
14	aaaaaaaaaa	ee79976c9380d5e337fc1c095ece8c8f22f91f306ceeb161fa51fecede2c4ba1	2025-04-11 17:31:11.65769
15	admin1234	ac9689e2272427085e35b9d3e3e8bed88cb3434828b43b86fc0596cad4c6e270	2025-04-11 21:46:24.549332
16	admin12345	41e5653fc7aeb894026d6bb7b2db7f65902b454945fa8fd65a6327047b5277fb	2025-04-11 22:14:51.339841
17	adm	ee79976c9380d5e337fc1c095ece8c8f22f91f306ceeb161fa51fecede2c4ba1	2025-04-11 22:43:57.398739
\.


--
-- TOC entry 4917 (class 0 OID 16650)
-- Dependencies: 220
-- Data for Name: wireguard_configs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wireguard_configs (id, user_id, location, private_key, public_key, config_data) FROM stdin;
\.


--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 221
-- Name: client_configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_configs_id_seq', 2, true);


--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 17, true);


--
-- TOC entry 4930 (class 0 OID 0)
-- Dependencies: 219
-- Name: wireguard_configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.wireguard_configs_id_seq', 1, false);


--
-- TOC entry 4765 (class 2606 OID 16673)
-- Name: client_configs client_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_configs
    ADD CONSTRAINT client_configs_pkey PRIMARY KEY (id);


--
-- TOC entry 4758 (class 2606 OID 16630)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4760 (class 2606 OID 16632)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4763 (class 2606 OID 16657)
-- Name: wireguard_configs wireguard_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wireguard_configs
    ADD CONSTRAINT wireguard_configs_pkey PRIMARY KEY (id);


--
-- TOC entry 4766 (class 1259 OID 16679)
-- Name: ix_client_configs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_client_configs_id ON public.client_configs USING btree (id);


--
-- TOC entry 4761 (class 1259 OID 16663)
-- Name: ix_wireguard_configs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_wireguard_configs_id ON public.wireguard_configs USING btree (id);


--
-- TOC entry 4768 (class 2606 OID 16674)
-- Name: client_configs client_configs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_configs
    ADD CONSTRAINT client_configs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4767 (class 2606 OID 16658)
-- Name: wireguard_configs wireguard_configs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wireguard_configs
    ADD CONSTRAINT wireguard_configs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2025-04-12 13:01:47

--
-- PostgreSQL database dump complete
--

