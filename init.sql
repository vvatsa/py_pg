CREATE EXTENSION vector;
CREATE EXTENSION multicorn;
create SERVER dummy FOREIGN DATA WRAPPER multicorn options ( wrapper 'dds.dummy_fdw.DummyFDW');
CREATE FOREIGN TABLE test (
    test character varying,
    test2 character varying
    ) server dummy options(
        num_rows '100'
    );

CREATE SERVER NP_NORMAL FOREIGN DATA WRAPPER multicorn options ( wrapper 'dds.numeric.NpNormal');
CREATE FOREIGN TABLE np_normal (
    idx integer,
    sample numeric,
    mean integer,
    std integer,
    size integer
) server NP_NORMAL options(
    mean '0',
    std '1',
    size '100'
);

CREATE SERVER CVE_DATA FOREIGN DATA WRAPPER multicorn options ( wrapper 'dds.web.CVEData');
CREATE FOREIGN TABLE cve_data (
    cve_id character varying,
    description character varying,
    score character varying
) server CVE_DATA;
