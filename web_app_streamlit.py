import streamlit as st
import json
import io
import os
import contextlib
import matplotlib.pyplot as plt
import pandas as pd
import concurrent.futures
import threading

# Configuración de la página
st.set_page_config(page_title="Gráficas del Notebook", layout="wide")
st.title("📊 Visualización de Gráficas desde `ParcialFinal.ipynb`")

def exec_with_timeout(code, globals_, timeout=10):
    """Ejecuta código con timeout, para evitar bloqueos largos."""
    def target():
        exec(code, globals_)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutError("Timeout: ejecución de celda demasiado larga")

def run_notebook_cell(cell_source):
    output_buffer = io.StringIO()
    figures = []

    exec_globals = {
        'pd': pd,
        'np': __import__('numpy'),
        'plt': plt,
        'st': st,
        'sns': __import__('seaborn') if 'seaborn' in cell_source else None,
    }

    try:
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
            plt.close('all')
            exec_with_timeout(cell_source, exec_globals, timeout=10)  # 10 segundos timeout
            figures = [plt.figure(i) for i in plt.get_fignums()]
    except TimeoutError as te:
        output_buffer.write(f"\n⚠️ Timeout: {te}\n")
    except Exception as e:
        output_buffer.write(f"\n⚠️ Error al ejecutar una celda: {e}\n")

    return figures

