import unittest
from flask import Flask
from flask_wtf import CSRFProtect
from forms import RegisterForm
from config import Config