#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the config arg parser module."""
from __future__ import print_function
from os import environ
from os.path import join, realpath, dirname
from argparse import ArgumentParser
from unittest import TestCase
from pacifica.configparser import ConfigArgParser


class TestConfigArgParse(TestCase):
    """Test the ConfigArgParse class."""

    @staticmethod
    def _rtfm_example():
        """The argparse example straight out of the docs."""
        parser = ArgumentParser(description='Process some integers.')
        parser.add_argument(
            'integers', metavar='N', type=int, nargs='+',
            help='an integer for the accumulator'
        )
        parser.add_argument(
            '--foo', dest='foo', default='blah',
            help='the foo argument'
        )
        parser.add_argument(
            '--sum', dest='accumulate', action='store_const',
            const=sum, default=max,
            help='sum the integers (default: find the max)'
        )
        return parser

    @classmethod
    def _group_example(cls):
        """Test argument groups and how it shows up in ini files."""
        parser = cls._rtfm_example()
        group_a = parser.add_argument_group('group-a')
        group_b = parser.add_argument_group('group-b')
        group_a.add_argument('--bar', help='bar help')
        group_b.add_argument('--fiz', help='fiz help')
        return parser

    def test_group_example(self):
        """Test config groups."""
        args = ConfigArgParser.configargparser(
            self._group_example(), {}, join(dirname(realpath(__file__)), 'group.ini'),
            'PACIFICA_CONFIGPARSE',
            ['1', '2']
        )
        self.assertEqual(args.fiz, '5432')
        self.assertEqual(args.bar, '5678')

    def test_simple_parser(self):
        """Test the RTFM argparse example."""
        args = ConfigArgParser.configargparser(
            self._rtfm_example(), {}, join(dirname(realpath(__file__)), 'example.ini'),
            'PACIFICA_CONFIGPARSE',
            ['1', '2']
        )
        self.assertEqual(args.accumulate, max)
        self.assertEqual(args.foo, 'blah')

    def test_env_cmd_parser(self):
        """Test that environment gets overridden by command line."""
        environ['PACIFICA_CONFIGPARSE_FOO'] = 'fiz'
        args = ConfigArgParser.configargparser(
            self._rtfm_example(), {}, join(dirname(realpath(__file__)), 'setfoo.ini'),
            'PACIFICA_CONFIGPARSE',
            ['--foo', 'biz', '1', '2']
        )
        self.assertEqual(args.integers, [1, 2])
        self.assertEqual(args.foo, 'biz')

    def test_env_parser(self):
        """Test that config gets overridden by environment."""
        environ['PACIFICA_CONFIGPARSE_FOO'] = 'fiz'
        args = ConfigArgParser.configargparser(
            self._rtfm_example(), {}, join(dirname(realpath(__file__)), 'setfoo.ini'),
            'PACIFICA_CONFIGPARSE',
            ['1', '2']
        )
        self.assertEqual(args.integers, [1, 2])
        self.assertEqual(args.foo, 'fiz')

    def test_config_parser(self):
        """Test that defaults get overridden by config."""
        args = ConfigArgParser.configargparser(
            self._rtfm_example(), {}, join(dirname(realpath(__file__)), 'setfoo.ini'),
            'PACIFICA_CONFIGPARSE',
            ['1', '2']
        )
        self.assertEqual(args.integers, [1, 2])
        self.assertEqual(args.foo, 'baz')

    def test_empty_config_file(self):
        """Test that defaults get overridden by config."""
        args = ConfigArgParser.configargparser(
            self._rtfm_example(), {}, join(dirname(realpath(__file__)), 'empty.ini'),
            'PACIFICA_CONFIGPARSE',
            ['1', '2']
        )
        self.assertEqual(args.integers, [1, 2])
        self.assertEqual(args.foo, 'blah')

    def test_notfound_config_file(self):
        """Test that defaults get overridden by config."""
        hit_exception = False
        try:
            ConfigArgParser.configargparser(
                self._rtfm_example(), {}, join(dirname(realpath(__file__)), 'notthere.ini'),
                'PACIFICA_CONFIGPARSE',
                ['1', '2']
            )
        except IOError:
            hit_exception = True
        self.assertTrue(hit_exception)
