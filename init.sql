CREATE EXTENSION multicorn;
create SERVER dummy FOREIGN DATA WRAPPER multicorn options ( wrapper 'dds.dummy_fdw.DummyFDW');
CREATE FOREIGN TABLE test (
    test character varying,
    test2 character varying
    ) server dummy options(
        num_rows '100'
    );
