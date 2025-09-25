CREATE EXTENSION multicorn;
create SERVER dds FOREIGN DATA WRAPPER multicorn options ( wrapper 'dds.dummy_fdw.DummyFDW');
CREATE FOREIGN TABLE test (
    test character varying,
    test2 character varying
    ) server dds;
