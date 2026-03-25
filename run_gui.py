import os
import re
import sys
import signal
import queue
import threading
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk

import tempfile
import xml.etree.ElementTree as ET
import json
import csv
from datetime import datetime

try:
    from fpdf import FPDF  # type: ignore
except Exception:
    FPDF = None

# =============================================================================
# Configuração inicial
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent
TEST_DIRS = [PROJECT_ROOT / "Testes", PROJECT_ROOT / "Testes_Mobile"]
VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"


def _require_project_venv():
    """Abort early if not running with the project's venv interpreter."""
    expected = VENV_PYTHON.resolve()
    current = Path(sys.executable).resolve()

    # Alert also when the venv python does not exist (setup issue).
    if not expected.exists() or current != expected:
        msg = (
            "Use o Python do venv para executar o GUI.\n"
            f"Esperado: {expected}\n"
            f"Atual:    {current}"
        )
        try:
            # Avoid full Tk init; show a simple error dialog if possible.
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Executor de Testes", msg)
            root.destroy()
        except Exception:
            print(msg, file=sys.stderr)
        sys.exit(1)


_require_project_venv()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =============================================================================
# Paleta visual
# =============================================================================
COLOR_BG = "#1F1F22"
COLOR_PANEL = "#2A2A2E"
COLOR_CARD = "#2E2E33"
COLOR_INPUT = "#18181B"
COLOR_BORDER = "#3A3A40"

COLOR_PRIMARY = "#2e5372"
COLOR_PRIMARY_HOVER = "#3b6a91"

COLOR_SUCCESS = "#3FAE5A"
COLOR_DANGER = "#C94B4B"
COLOR_DANGER_HOVER = "#B33E3E"

COLOR_TEXT = "#F5F5F5"
COLOR_TEXT_MUTED = "#C8C8CC"

COLOR_STATUS_IDLE = "#E0E0E0"
COLOR_STATUS_RUNNING = "#E3B341"
COLOR_STATUS_SUCCESS = "#3FAE5A"
COLOR_STATUS_ERROR = "#C94B4B"
COLOR_DISABLED = "#3A3A40"
COLOR_DISABLED_TEXT = "#8A8A90"
COLOR_PLACEHOLDER = "#2f2f33"
COLOR_PLACEHOLDER_TEXT = "#8A8A90"
COLOR_SCROLL = "#3b4a5a"
COLOR_SCROLL_HOVER = "#4b6278"

AMBIENTE_PLACEHOLDER = "Selecione a visualização"
GRID_PLACEHOLDER = "Selecione a plataforma"
NAVEGADOR_PLACEHOLDER = "Selecione o navegador"
SO_PLACEHOLDER = "Selecione o sistema"
DEVICE_PLACEHOLDER = "Selecione o dispositivo"
RESOLUTION_PLACEHOLDER = "Selecione a resolução"
TIMEOUT_PLACEHOLDER = "Selecione o timeout"

RESOLUTION_CHOICES = [
    ("1366 x 768", "1366x768"),
    ("1920 x 1080", "1920x1080"),
    ("1536 x 864", "1536x864"),
    ("1440 x 900", "1440x900"),
    ("1600 x 900", "1600x900"),
    ("1280 x 720", "1280x720"),
    ("1360 x 768", "1360x768"),
    ("1280 x 1024", "1280x1024"),
    ("1280 x 800", "1280x800"),
    ("1024 x 768", "1024x768"),
]
RESOLUTION_DISPLAY_TO_VALUE = {label: value for label, value in RESOLUTION_CHOICES}
CUSTOM_RESOLUTION_LABEL = "Outro (digitar)"

TIMEOUT_CHOICES = [(str(v), str(v)) for v in range(5, 61, 5)]
TIMEOUT_DISPLAY_TO_VALUE = {label: value for label, value in TIMEOUT_CHOICES}

DEVICE_GROUPS = {
    "384x832": ["iPhone 13 Mini"],
    "390x844": ["iPhone 12", "iPhone 13", "iPhone 14"],
    "393x852": ["iPhone 14 Pro", "iPhone 15", "iPhone 15 Pro"],
    "430x932": ["iPhone 14 Pro Max", "iPhone 15 Plus", "iPhone 15 Pro Max"],
    "414x896": ["iPhone 11"],
    "412x915": [
        "Samsung Galaxy S20 Ultra",
        "Samsung Galaxy Note 20",
        "Samsung Galaxy A51",
        "Samsung Galaxy A32",
        "Samsung Galaxy A31",
    ],
    "360x800": [
        "Samsung Galaxy S20",
        "Samsung Galaxy S21",
        "Samsung Galaxy S22",
        "Samsung Galaxy S23",
        "Samsung Galaxy S24",
        "Google Pixel 8",
        "Google Pixel 9",
    ],
    "393x873": [
        "Motorola Edge 30",
        "Xiaomi Redmi Note 13",
        "Samsung Galaxy A54",
    ],
    "432x960": [
        "Samsung Galaxy A73",
        "Samsung Galaxy A72",
        "Samsung Galaxy S21 FE",
    ],
    "440x956": [
        "Samsung Galaxy S22 Ultra",
        "Samsung Galaxy S23 Ultra",
        "Samsung Galaxy S24 Ultra",
    ],
}

DEVICE_CHOICES = [
    (name, resolution)
    for resolution, names in DEVICE_GROUPS.items()
    for name in names
]
DEVICE_DISPLAY_TO_NAME = {
    f"{name} ({resolution})": name for name, resolution in DEVICE_CHOICES
}
DEVICE_OPTION_VALUES = list(DEVICE_DISPLAY_TO_NAME.keys())
CUSTOM_DEVICE_LABEL = "Outro (digitar)"


# =============================================================================
# Estados globais
# =============================================================================
process = None
log_queue = queue.Queue()

all_test_files = []
left_test_vars = []
left_test_widgets = []

app = None
command_preview = None
log_box = None
status_label = None
left_selected_count_label = None

run_button = None
stop_button = None

total_value_label = None
passed_value_label = None
failed_value_label = None

left_tests_frame = None

test_filter_var = None
ambiente_var = None
grid_var = None
navegador_var = None
so_var = None
device_var = None
device_choice_var = None
custom_device_var = None
custom_device_entry = None
custom_device_label_widget = None
device_option_menu = None
timeout_var = None
timeout_choice_var = None
timeout_option_menu = None
resolution_var = None
resolution_choice_var = None
custom_resolution_var = None
custom_resolution_entry = None
custom_resolution_label_widget = None
resolution_option_menu = None
headless_var = None
custom_url_var = None
build_name_var = None
target_env_var = None
custom_url_label_widget = None
custom_url_entry_widget = None
ambiente_option_menu = None
grid_option_menu = None
navegador_option_menu = None
so_option_menu = None

clear_filter_button = None

test_results_by_status = {
    "total": [],
    "passed": [],
    "failed": [],
    "skipped": []
}

last_junit_xml_path = None
history_data = []
last_run_command = ""
last_selected_tests = []

HISTORY_FILE = PROJECT_ROOT / ".test_history.json"
history_window = None
history_selection_vars = {}
delete_selected_btn = None
delete_all_btn = None
history_start_day_var = None
history_start_month_var = None
history_start_year_var = None
history_end_day_var = None
history_end_month_var = None
history_end_year_var = None
today_checkbox_var = None


# =============================================================================
# Helpers
# =============================================================================
def get_python_executable():
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable


def extract_test_number(path_str):
    file_name = Path(path_str).name.lower()
    match = re.search(r"test_(\d+)", file_name)
    if match:
        return int(match.group(1))
    return 999999


def build_test_sort_key(path_str):
    path_obj = Path(path_str)
    file_name = path_obj.name.lower()
    return (
        extract_test_number(path_str),
        file_name,
        path_str.lower()
    )


def discover_tests():
    found = []

    for base_dir in TEST_DIRS:
        dir_tests = []

        if base_dir.exists():
            for file in base_dir.rglob("test_*.py"):
                try:
                    rel = file.relative_to(PROJECT_ROOT)
                    normalized = str(rel).replace("\\", "/")
                    dir_tests.append(normalized)
                except Exception:
                    dir_tests.append(str(file).replace("\\", "/"))

        dir_tests.sort(key=build_test_sort_key)
        found.extend(dir_tests)

    return found


def command_to_string(cmd):
    parts = []
    for item in cmd:
        if " " in item:
            parts.append(f'"{item}"')
        else:
            parts.append(item)
    return " ".join(parts)


def append_log(text):
    log_box.configure(state="normal")
    log_box.insert("end", text)
    log_box.see("end")
    log_box.configure(state="disabled")


def clear_logs():
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")


def set_command_preview(text):
    command_preview.configure(state="normal")
    command_preview.delete("1.0", "end")
    command_preview.insert("1.0", text)
    command_preview.configure(state="disabled")


def update_summary(total=0, passed=0, failed=0, skipped=0):
    total_value_label.configure(text=f"{getattr(total_value_label, 'base_text', 'Total')} - {total}")
    passed_value_label.configure(text=f"{getattr(passed_value_label, 'base_text', 'Passed')} - {passed}")
    failed_value_label.configure(text=f"{getattr(failed_value_label, 'base_text', 'Failed')} - {failed}")


def parse_pytest_summary(output_text):
    passed = 0
    failed = 0
    skipped = 0

    m = re.search(r"(\d+)\s+passed", output_text)
    if m:
        passed = int(m.group(1))

    m = re.search(r"(\d+)\s+failed", output_text)
    if m:
        failed = int(m.group(1))

    m = re.search(r"(\d+)\s+skipped", output_text)
    if m:
        skipped = int(m.group(1))

    total = passed + failed + skipped
    return total, passed, failed, skipped

def parse_junit_xml_results(xml_path):
    results = {
        "total": [],
        "passed": [],
        "failed": [],
        "skipped": []
    }

    if not xml_path or not Path(xml_path).exists():
        return results

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for testcase in root.iter("testcase"):
            classname = testcase.attrib.get("classname", "").replace(".", "/")
            name = testcase.attrib.get("name", "").strip()

            if classname:
                test_name = f"{classname}::{name}"
            else:
                test_name = name

            results["total"].append(test_name)

            if testcase.find("failure") is not None or testcase.find("error") is not None:
                results["failed"].append(test_name)
            elif testcase.find("skipped") is not None:
                results["skipped"].append(test_name)
            else:
                results["passed"].append(test_name)

    except Exception as e:
        append_log(f"\n[WARN] Não foi possível ler o junit xml: {e}\n")

    return results


def show_tests_by_status(status_key, title):
    tests = test_results_by_status.get(status_key, [])

    window = ctk.CTkToplevel(app)
    window.title(title)
    window.geometry("650x420")
    window.configure(fg_color=COLOR_BG)

    window.lift()
    window.attributes("-topmost", True)
    window.after(200, lambda: window.attributes("-topmost", False))
    window.focus_force()

    container = ctk.CTkFrame(
        window,
        fg_color=COLOR_PANEL,
        corner_radius=12,
        border_color=COLOR_BORDER,
        border_width=1
    )
    container.pack(fill="both", expand=True, padx=20, pady=20)

    header = ctk.CTkLabel(
        container,
        text=f"{title} ({len(tests)})",
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=20, weight="bold")
    )
    header.pack(anchor="w", padx=16, pady=(16, 8))

    box = ctk.CTkTextbox(
        container,
        fg_color=COLOR_INPUT,
        border_width=1,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    box.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    if tests:
        formatted_tests = [format_result_test_name(test) for test in tests]
        box.insert("1.0", "\n".join(formatted_tests))
    else:
        box.insert("1.0", "Nenhum teste encontrado para este grupo.")

    box.configure(state="disabled")


def clear_filter():
    test_filter_var.set("")
    rebuild_left_tests("")

    if clear_filter_button is not None:
        clear_filter_button.grid_remove()


def format_result_test_name(test_name):
    if "::" in test_name:
        return test_name.split("::", 1)[1]
    return test_name


def format_selected_test(path_str):
    try:
        stem = Path(path_str).stem
        if stem.lower().startswith("test_"):
            return stem[5:]
        return stem
    except Exception:
        return path_str


def set_status(message, status_type="idle"):
    color_map = {
        "idle": COLOR_STATUS_IDLE,
        "running": COLOR_STATUS_RUNNING,
        "success": COLOR_STATUS_SUCCESS,
        "error": COLOR_STATUS_ERROR,
    }

    status_label.configure(
        text=f"Status: {message}",
        text_color=color_map.get(status_type, COLOR_STATUS_IDLE)
    )


def format_timestamp(ts: str):
    """Return DD/MM/YYYY HH:MM for display; fallback to raw string."""
    try:
        return datetime.fromisoformat(ts).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return ts


def load_history():
    global history_data
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        except Exception:
            history_data = []
    else:
        history_data = []


def save_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        append_log(f"\n[WARN] NÃ£o foi possÃ­vel salvar histÃ³rico: {e}\n")


def add_history_entry(entry):
    global history_data
    history_data.insert(0, entry)
    if len(history_data) > 500:
        history_data = history_data[:500]
    save_history()


def filter_history_items(start_date=None, end_date=None, status_filter="all"):
    items = history_data

    def to_date(s):
        try:
            return datetime.fromisoformat(s).date()
        except Exception:
            return None

    start_dt = start_date
    end_dt = end_date

    filtered = []
    for it in items:
        ts_date = to_date(it.get("timestamp", ""))
        status_ok = status_filter in ("all", "", None) or it.get("status") == status_filter
        date_ok = True
        if start_dt and ts_date:
            date_ok = ts_date >= start_dt
        if end_dt and ts_date and date_ok:
            date_ok = ts_date <= end_dt
        if status_ok and date_ok:
            filtered.append(it)
    return filtered


def delete_selected_history():
    global history_data
    if not history_selection_vars:
        return

    selected_ids = {key for key, var in history_selection_vars.items() if var.get()}
    if not selected_ids:
        return

    if not messagebox.askyesno("Confirmar", "Excluir os históricos selecionados?"):
        return

    history_data = [it for it in history_data if (it.get("id") or it.get("timestamp")) not in selected_ids]
    save_history()
    rebuild_history_table()


def delete_all_history():
    global history_data
    if not history_data:
        return
    if not messagebox.askyesno("Confirmar", "Excluir TODO o histórico?"):
        return
    history_data = []
    save_history()
    rebuild_history_table()


def update_delete_buttons_state():
    if delete_selected_btn is None:
        return
    has_selection = any(var.get() for var in history_selection_vars.values())
    delete_selected_btn.configure(state="normal" if has_selection else "disabled")


def on_device_choice(value):
    if value == DEVICE_PLACEHOLDER:
        custom_device_label_widget.grid_remove()
        custom_device_entry.grid_remove()
        device_var.set("")
        apply_menu_style(device_option_menu, True)
        return

    # Atualiza o valor final e exibe/oculta a entrada personalizada
    if value == CUSTOM_DEVICE_LABEL:
        custom_device_label_widget.grid()
        custom_device_entry.grid()
        custom_device_entry.configure(state="normal")
        custom_device_entry.delete(0, "end")
        custom_device_var.set("")
        device_var.set("")
    else:
        custom_device_label_widget.grid_remove()
        custom_device_entry.grid_remove()
        device_var.set(DEVICE_DISPLAY_TO_NAME.get(value, value))
    apply_menu_style(device_option_menu, False)


def on_custom_device_change(*_args):
    if device_choice_var.get() == CUSTOM_DEVICE_LABEL:
        device_var.set(custom_device_var.get().strip())


def on_resolution_choice(value):
    if value == RESOLUTION_PLACEHOLDER:
        custom_resolution_label_widget.grid_remove()
        custom_resolution_entry.grid_remove()
        resolution_var.set("")
        apply_menu_style(resolution_option_menu, True)
        return

    if value == CUSTOM_RESOLUTION_LABEL:
        custom_resolution_label_widget.grid()
        custom_resolution_entry.grid()
        custom_resolution_entry.configure(state="normal")
        custom_resolution_entry.delete(0, "end")
        custom_resolution_var.set("")
        resolution_var.set("")
    else:
        custom_resolution_label_widget.grid_remove()
        custom_resolution_entry.grid_remove()
        resolution_var.set(RESOLUTION_DISPLAY_TO_VALUE.get(value, value).replace(" ", ""))
    apply_menu_style(resolution_option_menu, False)


def on_custom_resolution_change(*_args):
    if resolution_choice_var.get() == CUSTOM_RESOLUTION_LABEL:
        resolution_var.set(custom_resolution_var.get().strip().replace(" ", ""))


def build_date_from_select(day_val, month_val, year_val):
    if not day_val or not month_val or not year_val:
        return None
    if day_val in ("DD", "") or month_val in ("MM", "") or year_val in ("AAAA", ""):
        return None
    try:
        return datetime(int(year_val), int(month_val), int(day_val)).date()
    except Exception:
        return None


def get_history_year_choices():
    years = {datetime.now().year}
    for item in history_data:
        ts = item.get("timestamp")
        try:
            years.add(datetime.fromisoformat(ts).year)
        except Exception:
            continue
    ordered = ["AAAA"] + [str(y) for y in sorted(years)]
    return ordered


def apply_menu_style(menu, is_placeholder):
    if not menu:
        return
    if is_placeholder:
        menu.configure(
            fg_color=COLOR_PLACEHOLDER,
            button_color=COLOR_PLACEHOLDER,
            button_hover_color=COLOR_PLACEHOLDER,
            text_color=COLOR_PLACEHOLDER_TEXT,
            dropdown_text_color=COLOR_PLACEHOLDER_TEXT,
        )
    else:
        menu.configure(
            fg_color=COLOR_PRIMARY,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            dropdown_text_color=COLOR_TEXT,
        )


def on_option_placeholder_change(var, placeholder, menu):
    apply_menu_style(menu, var.get() == placeholder)


def on_timeout_choice(value):
    if value == TIMEOUT_PLACEHOLDER:
        timeout_var.set("")
    else:
        timeout_var.set(TIMEOUT_DISPLAY_TO_VALUE.get(value, value))
    apply_menu_style(timeout_option_menu, value == TIMEOUT_PLACEHOLDER)


def on_ambiente_change(*_args):
    env = (ambiente_var.get() or "").lower()
    is_placeholder = ambiente_var.get() == AMBIENTE_PLACEHOLDER
    apply_menu_style(ambiente_option_menu, is_placeholder)

    # Limpa seleções incompatíveis ao trocar de ambiente
    if env in ("desktop", "mobile"):
        for var, path in left_test_vars:
            if (env == "desktop" and path.startswith("Testes_Mobile/")) or (env == "mobile" and path.startswith("Testes/")):
                var.set(False)
        rebuild_left_tests(test_filter_var.get())
        update_left_selected_counter()

    # Reset: desabilita ambos antes de aplicar regras
    def disable_device():
        device_choice_var.set(DEVICE_PLACEHOLDER)
        device_var.set("")
        custom_device_var.set("")
        if device_option_menu:
            device_option_menu.configure(
                state="disabled",
                fg_color=COLOR_DISABLED,
                button_color=COLOR_DISABLED,
                button_hover_color=COLOR_DISABLED,
                text_color=COLOR_DISABLED_TEXT,
                dropdown_text_color=COLOR_DISABLED_TEXT,
            )
        if custom_device_label_widget:
            custom_device_label_widget.grid_remove()
        if custom_device_entry:
            custom_device_entry.configure(
                state="disabled",
                fg_color=COLOR_DISABLED,
                border_color=COLOR_BORDER,
                text_color=COLOR_DISABLED_TEXT,
            )
            custom_device_entry.grid_remove()

    def disable_resolution():
        resolution_choice_var.set(RESOLUTION_PLACEHOLDER)
        resolution_var.set("")
        custom_resolution_var.set("")
        if resolution_option_menu:
            resolution_option_menu.configure(
                state="disabled",
                fg_color=COLOR_DISABLED,
                button_color=COLOR_DISABLED,
                button_hover_color=COLOR_DISABLED,
                text_color=COLOR_DISABLED_TEXT,
                dropdown_text_color=COLOR_DISABLED_TEXT,
            )
        if custom_resolution_label_widget:
            custom_resolution_label_widget.grid_remove()
        if custom_resolution_entry:
            custom_resolution_entry.configure(
                state="disabled",
                fg_color=COLOR_DISABLED,
                border_color=COLOR_BORDER,
                text_color=COLOR_DISABLED_TEXT,
            )
            custom_resolution_entry.grid_remove()

    disable_device()
    disable_resolution()

    if is_placeholder:
        return

    if env == "desktop":
        # Resolution habilitado
        if resolution_option_menu:
            resolution_option_menu.configure(
                state="normal",
                fg_color=COLOR_PRIMARY,
                button_color=COLOR_PRIMARY,
                button_hover_color=COLOR_PRIMARY_HOVER,
                text_color=COLOR_TEXT,
                dropdown_text_color=COLOR_TEXT,
            )
        if custom_resolution_entry:
            custom_resolution_entry.configure(
                state="normal",
                fg_color=COLOR_INPUT,
                border_color=COLOR_BORDER,
                text_color=COLOR_TEXT,
            )
        resolution_choice_var.set(RESOLUTION_PLACEHOLDER)
        resolution_var.set("")
        custom_resolution_var.set("")

    elif env == "mobile":
        # Device habilitado
        if device_option_menu:
            device_option_menu.configure(
                state="normal",
                fg_color=COLOR_PRIMARY,
                button_color=COLOR_PRIMARY,
                button_hover_color=COLOR_PRIMARY_HOVER,
                text_color=COLOR_TEXT,
                dropdown_text_color=COLOR_TEXT,
            )
        if custom_device_entry:
            custom_device_entry.configure(
                state="normal",
                fg_color=COLOR_INPUT,
                border_color=COLOR_BORDER,
                text_color=COLOR_TEXT,
            )
        device_choice_var.set(DEVICE_PLACEHOLDER)
        device_var.set("")
        custom_device_var.set("")
    else:
        # fallback: habilita ambos
        if device_option_menu:
            device_option_menu.configure(state="normal")
            apply_menu_style(device_option_menu, device_choice_var.get() == DEVICE_PLACEHOLDER)
        if custom_device_entry:
            custom_device_entry.configure(
                state="normal",
                fg_color=COLOR_INPUT,
                border_color=COLOR_BORDER,
                text_color=COLOR_TEXT,
            )
            custom_device_entry.grid_remove()
        if resolution_option_menu:
            resolution_option_menu.configure(state="normal")
            apply_menu_style(resolution_option_menu, resolution_choice_var.get() == RESOLUTION_PLACEHOLDER)
        if custom_resolution_entry:
            custom_resolution_entry.configure(
                state="normal",
                fg_color=COLOR_INPUT,
                border_color=COLOR_BORDER,
                text_color=COLOR_TEXT,
            )
            custom_resolution_entry.grid_remove()


# =============================================================================
# Testes da coluna esquerda
# =============================================================================
section_collapsed = {
    ("Desktop", "Default"): False,
    ("Desktop", "Sul"): False,
    ("Desktop", "Outros"): False,
    ("Mobile", "Default"): False,
    ("Mobile", "Sul"): False,
    ("Mobile", "Outros"): False,
}


def toggle_section(platform, subgroup):
    section_collapsed[(platform, subgroup)] = not section_collapsed[(platform, subgroup)]
    rebuild_left_tests(test_filter_var.get())


def update_left_selected_counter():
    total = len(left_test_vars)
    checked = sum(1 for var, _ in left_test_vars if var.get())
    left_selected_count_label.configure(text=f"Selecionados: {checked} de {total}")


def clear_left_tests():
    for widget in left_tests_frame.winfo_children():
        widget.destroy()

    left_test_vars.clear()
    left_test_widgets.clear()


def format_test_display_name(test_path):
    try:
        stem = Path(test_path).stem
        if stem.lower().startswith("test_"):
            return stem[5:]
        return stem
    except Exception:
        return test_path


def rebuild_left_tests(filter_text=""):
    clear_left_tests()

    filter_text = (filter_text or "").strip().lower()

    ambiente = (ambiente_var.get() or "").lower()
    ambiente_filter = None
    if ambiente == "desktop":
        ambiente_filter = "Desktop"
    elif ambiente == "mobile":
        ambiente_filter = "Mobile"

    grouped = {
        "Desktop": {"Default": [], "Sul": [], "Outros": []},
        "Mobile": {"Default": [], "Sul": [], "Outros": []}
    }

    for test_path in all_test_files:
        display_name = format_test_display_name(test_path)

        if filter_text and filter_text not in display_name.lower():
            continue

        normalized_path = test_path.replace("\\", "/").lower()

        if normalized_path.startswith("testes_mobile/"):
            platform = "Mobile"
        else:
            platform = "Desktop"

        if ambiente_filter and platform != ambiente_filter:
            continue

        if "/default/" in normalized_path:
            subgroup = "Default"
        elif "/sul/" in normalized_path:
            subgroup = "Sul"
        else:
            subgroup = "Outros"

        grouped[platform][subgroup].append((test_path, display_name))

    current_row = 0

    def add_group_title(title, row):
        label = ctk.CTkLabel(
            left_tests_frame,
            text=title,
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        label.grid(row=row, column=0, sticky="w", padx=8, pady=(12, 6))
        return row + 1

    def add_subtitle_button(platform, subgroup, row, count):
        collapsed = section_collapsed[(platform, subgroup)]
        icon = "▶" if collapsed else "▼"

        btn = ctk.CTkButton(
            left_tests_frame,
            text=f"{icon} {subgroup} ({count})",
            command=lambda p=platform, s=subgroup: toggle_section(p, s),
            fg_color="transparent",
            hover_color=COLOR_CARD,
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        btn.grid(row=row, column=0, sticky="ew", padx=14, pady=(6, 4))
        return row + 1

    def add_test_checkbox(original_path, display_name, row):
        var = tk.BooleanVar(value=False)

        cb = ctk.CTkCheckBox(
            left_tests_frame,
            text=display_name,
            variable=var,
            command=update_left_selected_counter,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        cb.grid(row=row, column=0, sticky="w", padx=28, pady=4)

        left_test_vars.append((var, original_path))
        left_test_widgets.append(cb)
        return row + 1

    for platform in ["Desktop", "Mobile"]:
        has_any_test = any(grouped[platform][key] for key in ["Default", "Sul", "Outros"])
        if not has_any_test:
            continue

        current_row = add_group_title(platform, current_row)

        for subgroup in ["Default", "Sul", "Outros"]:
            tests = grouped[platform][subgroup]
            if not tests:
                continue

            current_row = add_subtitle_button(platform, subgroup, current_row, len(tests))

            if section_collapsed[(platform, subgroup)]:
                continue

            for original_path, display_name in tests:
                current_row = add_test_checkbox(original_path, display_name, current_row)

    update_left_selected_counter()


def apply_filter():
    filter_text = test_filter_var.get().strip()
    rebuild_left_tests(filter_text)

    if clear_filter_button is not None:
        if filter_text:
            clear_filter_button.grid()
        else:
            clear_filter_button.grid_remove()


def select_all_tests():
    for var, _ in left_test_vars:
        var.set(True)
    update_left_selected_counter()


def deselect_all_tests():
    for var, _ in left_test_vars:
        var.set(False)
    update_left_selected_counter()


def get_selected_tests():
    return [path for var, path in left_test_vars if var.get()]


# =============================================================================
# Montagem do comando
# =============================================================================
def build_pytest_command():
    global last_junit_xml_path
    cmd = [get_python_executable(), "-m", "pytest"]

    selected_tests = get_selected_tests()
    if selected_tests:
        cmd.extend(selected_tests)

    # Paralelismo automático baseado na quantidade de testes
    num_tests = len(selected_tests)

    max_workers = 6  # limite seguro

    num_tests = len(selected_tests)

    if num_tests > 1:
        workers = min(num_tests, max_workers)
        cmd.extend(["-n", str(workers)])

    ambiente = ambiente_var.get().strip()
    grid = grid_var.get().strip()
    navegador = navegador_var.get().strip()
    so = so_var.get().strip()
    device = device_var.get().strip()
    timeout = timeout_var.get().strip()
    resolution = resolution_var.get().strip()
    headless = headless_var.get()
    build_name = build_name_var.get().strip() if 'build_name_var' in globals() else ""
    target_env = target_env_var.get().strip() if 'target_env_var' in globals() else ""
    custom_url = custom_url_var.get().strip() if 'custom_url_var' in globals() else ""

    if target_env.lower() == "outro" and not custom_url:
        messagebox.showerror("Ambiente", "Selecione 'Outro' apenas informando uma URL custom.")
        return None

    if ambiente and ambiente != AMBIENTE_PLACEHOLDER:
        cmd.extend(["--ambiente", ambiente])
    if grid and grid != GRID_PLACEHOLDER:
        cmd.extend(["--grid", grid])
    if navegador and navegador != NAVEGADOR_PLACEHOLDER:
        cmd.extend(["--navegador", navegador])
    if so and so != SO_PLACEHOLDER:
        cmd.extend(["--so", so])

    if timeout and timeout_choice_var.get() != TIMEOUT_PLACEHOLDER:
        cmd.extend(["--timeout", timeout])

    if resolution and resolution_choice_var.get() != RESOLUTION_PLACEHOLDER:
        cmd.extend(["--resolution", resolution])

    if device and device_choice_var.get() != DEVICE_PLACEHOLDER:
        cmd.extend(["--device", device])

    if headless:
        cmd.append("--headless")

    if build_name:
        cmd.extend(["--build-name", build_name])

    if target_env:
        cmd.extend(["--target-env", target_env])
    if custom_url:
        cmd.extend(["--base-url", custom_url])

    temp_xml = Path(tempfile.gettempdir()) / "pytest_gui_results.xml"
    last_junit_xml_path = str(temp_xml)
    cmd.extend(["--junitxml", last_junit_xml_path])

    return cmd


def preview_command():
    cmd = build_pytest_command()
    if not cmd:
        return
    set_command_preview(command_to_string(cmd))


def validate_before_run():
    selected_tests = get_selected_tests()
    if not selected_tests:
        messagebox.showwarning("Aviso", "Selecione pelo menos um teste.")
        return False
    return True


# =============================================================================
# Execução
# =============================================================================
def run_tests():
    global process, test_results_by_status, last_run_command, last_selected_tests

    if process and process.poll() is None:
        messagebox.showwarning("Aviso", "Já existe uma execução em andamento.")
        return

    if not validate_before_run():
        return

    python_exec = get_python_executable()
    if not Path(python_exec).exists():
        messagebox.showerror("Erro", "Não foi encontrado um executável Python válido.")
        return

    cmd = build_pytest_command()
    if not cmd:
        return
    cmd_text = command_to_string(cmd)
    last_run_command = cmd_text
    last_selected_tests = get_selected_tests()

    set_command_preview(cmd_text)
    clear_logs()
    test_results_by_status = {
        "total": [],
        "passed": [],
        "failed": [],
        "skipped": []
    }
    update_summary(0, 0, 0, 0)

    append_log(f"[INFO] Python em uso: {python_exec}\n")
    if VENV_PYTHON.exists():
        append_log("[INFO] Ambiente virtual .venv detectado.\n")
    else:
        append_log("[WARN] .venv não encontrado. Usando Python atual.\n")

    append_log(f"[INFO] Comando:\n{cmd_text}\n\n")

    set_status("executando testes...", "running")
    run_button.configure(state="disabled")
    stop_button.configure(state="normal")

    try:
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

        process = subprocess.Popen(
            cmd,
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            creationflags=creationflags
        )

        thread = threading.Thread(target=read_process_output, daemon=True)
        thread.start()

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível iniciar a execução.\n\n{e}")
        set_status("erro ao iniciar", "error")
        run_button.configure(state="normal")
        stop_button.configure(state="disabled")


def read_process_output():
    global process, test_results_by_status

    if not process or not process.stdout:
        return

    full_output = []

    for line in process.stdout:
        full_output.append(line)
        log_queue.put(("log", line))

    return_code = process.wait()
    final_output = "".join(full_output)
    total, passed, failed, skipped = parse_pytest_summary(final_output)
    test_results_by_status = parse_junit_xml_results(last_junit_xml_path)

    log_queue.put(("summary", (total, passed, failed, skipped)))
    log_queue.put(("finished", return_code))

    status = "passed" if return_code == 0 else "failed"
    timestamp = datetime.now().isoformat(timespec="seconds")
    formatted_selected = [format_selected_test(t) for t in last_selected_tests]
    passed_list = [format_result_test_name(t) for t in test_results_by_status.get("passed", [])]
    failed_list = [format_result_test_name(t) for t in test_results_by_status.get("failed", [])]
    skipped_list = [format_result_test_name(t) for t in test_results_by_status.get("skipped", [])]
    entry = {
        "id": timestamp,
        "timestamp": timestamp,
        "status": status,
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "grid": grid_var.get().strip(),
        "ambiente": ambiente_var.get().strip(),
        "navegador": navegador_var.get().strip(),
        "so": so_var.get().strip(),
        "device": device_var.get().strip(),
        "resolution": resolution_var.get().strip(),
        "headless": bool(headless_var.get()),
        "target_env": target_env_var.get().strip(),
        "build_name": build_name_var.get().strip(),
        "command": last_run_command,
        "tests": formatted_selected,
        "tests_passed": passed_list,
        "tests_failed": failed_list,
        "tests_skipped": skipped_list,
    }
    add_history_entry(entry)
    log_queue.put(("history_updated", None))


def stop_tests():
    global process

    if not process or process.poll() is not None:
        return

    try:
        set_status("interrompendo execução...", "running")
        append_log("\n[INFO] Tentando encerrar a execução...\n")

        # 1) Tenta interrupção estilo console no Windows
        if os.name == "nt":
            try:
                process.send_signal(signal.CTRL_BREAK_EVENT)
                append_log("[INFO] Sinal CTRL_BREAK_EVENT enviado.\n")
                process.wait(timeout=3)
            except Exception as e:
                append_log(f"[WARN] Falha ao enviar CTRL_BREAK_EVENT: {e}\n")

            # 2) Se ainda estiver vivo, tenta terminate()
            if process.poll() is None:
                try:
                    process.terminate()
                    append_log("[INFO] terminate() enviado ao processo.\n")
                    process.wait(timeout=3)
                except Exception as e:
                    append_log(f"[WARN] Falha no terminate(): {e}\n")

            # 3) Se ainda estiver vivo, mata a árvore inteira
            if process.poll() is None:
                try:
                    subprocess.run(
                        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                        check=False,
                        capture_output=True,
                        text=True
                    )
                    append_log("[INFO] taskkill executado para encerrar a árvore de processos.\n")
                except Exception as e:
                    append_log(f"[ERRO] Falha no taskkill: {e}\n")

        else:
            # Linux/macOS
            try:
                process.terminate()
                append_log("[INFO] terminate() enviado ao processo.\n")
                process.wait(timeout=3)
            except Exception as e:
                append_log(f"[WARN] Falha no terminate(): {e}\n")

            if process.poll() is None:
                try:
                    process.kill()
                    append_log("[INFO] kill() enviado ao processo.\n")
                except Exception as e:
                    append_log(f"[ERRO] Falha no kill(): {e}\n")

    except Exception as e:
        append_log(f"\n[ERRO] Não foi possível parar a execução: {e}\n")


def poll_log_queue():
    global process

    try:
        while True:
            item_type, payload = log_queue.get_nowait()

            if item_type == "log":
                append_log(payload)

            elif item_type == "summary":
                total, passed, failed, skipped = payload
                update_summary(total, passed, failed, skipped)

            elif item_type == "finished":
                return_code = payload
                run_button.configure(state="normal")
                stop_button.configure(state="disabled")

                if return_code == 0:
                    set_status("execução concluída com sucesso", "success")
                else:
                    set_status("execução finalizada com falhas", "error")

                append_log(f"\n[PROCESSO FINALIZADO] Código de saída: {return_code}\n")

            elif item_type == "history_updated":
                rebuild_history_table()

    except queue.Empty:
        pass

    app.after(100, poll_log_queue)


# =============================================================================
# Componentes visuais
# =============================================================================
def create_summary_card(parent, title, value_text, column, status_key):
    card_color_map = {
        "total": COLOR_CARD,
        "passed": "#1f4d2e",
        "failed": "#5a2323",
    }

    hover_color_map = {
        "total": COLOR_PANEL,
        "passed": "#27643b",
        "failed": "#6b2a2a",
    }

    card = ctk.CTkFrame(
        parent,
        fg_color=card_color_map.get(status_key, COLOR_CARD),
        corner_radius=10,
        border_color=COLOR_BORDER,
        border_width=1,
        cursor="hand2",
        width=100,
        height=36
    )
    card.grid(row=0, column=column, padx=6, pady=0)
    card.grid_propagate(False)

    title_label = ctk.CTkLabel(
        card,
        text=title,
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=11, weight="bold")
    )
    title_label.place(relx=0.5, rely=0.5, anchor="center")
    title_label.base_text = title.split(" -")[0]
    value_label = title_label  # usamos o próprio título para atualizar o número

    def on_click(_event=None):
        show_tests_by_status(status_key, title)

    def on_enter(_event=None):
        card.configure(fg_color=hover_color_map.get(status_key, COLOR_PANEL), border_width=2)
        card.grid_configure(pady=0)

    def on_leave(_event=None):
        card.configure(fg_color=card_color_map.get(status_key, COLOR_CARD), border_width=1)
        card.grid_configure(pady=0)

    for widget in (card, title_label):
        widget.bind("<Button-1>", on_click)
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    return value_label


def create_labeled_option(parent, label_text, variable, values, row, column):
    label = ctk.CTkLabel(
        parent,
        text=label_text,
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    label.grid(row=row, column=column, padx=10, pady=(4, 4), sticky="w")

    option = ctk.CTkOptionMenu(
        parent,
        variable=variable,
        values=values,
        fg_color=COLOR_PRIMARY,
        button_color=COLOR_PRIMARY,
        button_hover_color=COLOR_PRIMARY_HOVER,
        dropdown_fg_color=COLOR_PANEL,
        dropdown_hover_color=COLOR_PRIMARY_HOVER,
        dropdown_text_color=COLOR_TEXT,
        text_color=COLOR_TEXT
    )
    option.grid(row=row + 1, column=column, padx=10, pady=(0, 10), sticky="ew")
    return option


def create_labeled_entry(parent, label_text, variable, row, column, placeholder=""):
    label = ctk.CTkLabel(
        parent,
        text=label_text,
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    label.grid(row=row, column=column, padx=10, pady=(4, 4), sticky="w")

    entry = ctk.CTkEntry(
        parent,
        textvariable=variable,
        placeholder_text=placeholder,
        fg_color=COLOR_INPUT,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    entry.grid(row=row + 1, column=column, padx=10, pady=(0, 10), sticky="ew")


def create_device_selector(parent, row, column):
    global device_option_menu, custom_device_label_widget, custom_device_entry

    label = ctk.CTkLabel(
        parent,
        text="Dispositivos Mobile",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    label.grid(row=row, column=column, padx=10, pady=(4, 4), sticky="w")

    device_option_menu = ctk.CTkOptionMenu(
        parent,
        variable=device_choice_var,
        values=[DEVICE_PLACEHOLDER] + DEVICE_OPTION_VALUES + [CUSTOM_DEVICE_LABEL],
        command=on_device_choice,
        fg_color=COLOR_PLACEHOLDER,
        button_color=COLOR_PLACEHOLDER,
        button_hover_color=COLOR_PLACEHOLDER,
        dropdown_fg_color=COLOR_PANEL,
        dropdown_hover_color=COLOR_PRIMARY_HOVER,
        dropdown_text_color=COLOR_PLACEHOLDER_TEXT,
        text_color=COLOR_PLACEHOLDER_TEXT
    )
    device_option_menu.grid(row=row + 1, column=column, padx=10, pady=(0, 10), sticky="ew")

    custom_device_label_widget = ctk.CTkLabel(
        parent,
        text="Digite outro Device",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=13)
    )
    custom_device_label_widget.grid(row=row + 2, column=column, padx=10, pady=(0, 2), sticky="w")
    custom_device_label_widget.grid_remove()

    custom_device_entry = ctk.CTkEntry(
        parent,
        textvariable=custom_device_var,
        fg_color=COLOR_INPUT,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    custom_device_entry.grid(row=row + 3, column=column, padx=10, pady=(0, 10), sticky="ew")
    custom_device_entry.grid_remove()


def create_resolution_selector(parent, row, column):
    global resolution_option_menu, custom_resolution_label_widget, custom_resolution_entry

    label = ctk.CTkLabel(
        parent,
        text="Resolução Desktop",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    label.grid(row=row, column=column, padx=10, pady=(4, 4), sticky="w")

    resolution_option_menu = ctk.CTkOptionMenu(
        parent,
        variable=resolution_choice_var,
        values=[RESOLUTION_PLACEHOLDER] + [label for label, _ in RESOLUTION_CHOICES] + [CUSTOM_RESOLUTION_LABEL],
        command=on_resolution_choice,
        fg_color=COLOR_PLACEHOLDER,
        button_color=COLOR_PLACEHOLDER,
        button_hover_color=COLOR_PLACEHOLDER,
        dropdown_fg_color=COLOR_PANEL,
        dropdown_hover_color=COLOR_PRIMARY_HOVER,
        dropdown_text_color=COLOR_PLACEHOLDER_TEXT,
        text_color=COLOR_PLACEHOLDER_TEXT
    )
    resolution_option_menu.grid(row=row + 1, column=column, padx=10, pady=(0, 10), sticky="ew")

    custom_resolution_label_widget = ctk.CTkLabel(
        parent,
        text="Digite outra resolução",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=13)
    )
    custom_resolution_label_widget.grid(row=row + 2, column=column, padx=10, pady=(0, 2), sticky="w")
    custom_resolution_label_widget.grid_remove()

    custom_resolution_entry = ctk.CTkEntry(
        parent,
        textvariable=custom_resolution_var,
        fg_color=COLOR_INPUT,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    custom_resolution_entry.grid(row=row + 3, column=column, padx=10, pady=(0, 10), sticky="ew")
    custom_resolution_entry.grid_remove()


def create_timeout_selector(parent, row, column):
    global timeout_option_menu

    label = ctk.CTkLabel(
        parent,
        text="Timeout",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    label.grid(row=row, column=column, padx=10, pady=(4, 4), sticky="w")

    timeout_option_menu = ctk.CTkOptionMenu(
        parent,
        variable=timeout_choice_var,
        values=[TIMEOUT_PLACEHOLDER] + [label for label, _ in TIMEOUT_CHOICES],
        command=on_timeout_choice,
        fg_color=COLOR_PLACEHOLDER,
        button_color=COLOR_PLACEHOLDER,
        button_hover_color=COLOR_PLACEHOLDER,
        dropdown_fg_color=COLOR_PANEL,
        dropdown_hover_color=COLOR_PRIMARY_HOVER,
        dropdown_text_color=COLOR_PLACEHOLDER_TEXT,
        text_color=COLOR_PLACEHOLDER_TEXT
    )
    timeout_option_menu.grid(row=row + 1, column=column, padx=10, pady=(0, 10), sticky="ew")


# =============================================================================
# Historico
# =============================================================================
history_rows_frame = None
history_status_filter_var = None
history_start_filter_var = None
history_end_filter_var = None
history_empty_label = None


def on_history_filter_change(*_args):
    rebuild_history_table()


def export_history_csv():
    items = get_filtered_history()
    if not items:
        messagebox.showinfo("Exportar CSV", "Nenhum item para exportar.")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")],
        initialfile="historico_testes.csv"
    )
    if not path:
        return
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "datetime", "status", "total", "passed", "failed",
                "grid", "ambiente", "navegador", "so", "amb_exec",
                "mobile_device", "desktop_resolution", "headless", "tests", "command"
            ])
            for it in items:
                ambiente_exec = it.get("ambiente", "")
                mobile_device = it.get("device", "") if ambiente_exec == "mobile" else ""
                desktop_resolution = it.get("resolution", "") if ambiente_exec == "desktop" else ""
                writer.writerow([
                    it.get("timestamp", ""),
                    it.get("status", ""),
                    it.get("total", 0),
                    it.get("passed", 0),
                    it.get("failed", 0),
                    it.get("grid", ""),
                    it.get("ambiente", ""),
                    it.get("navegador", ""),
                    it.get("so", ""),
                    it.get("target_env", ""),
                    mobile_device,
                    desktop_resolution,
                    str(it.get("headless", False)),
                    ";".join(it.get("tests", [])),
                    it.get("command", ""),
                ])
        messagebox.showinfo("Exportar CSV", f"CSV salvo em:\n{path}")
    except Exception as e:
        messagebox.showerror("Exportar CSV", f"Erro ao salvar CSV:\n{e}")


def export_history_pdf():
    if FPDF is None:
        messagebox.showerror("Exportar PDF", "Pacote fpdf2 nÃ£o estÃ¡ instalado.")
        return
    items = get_filtered_history()
    if not items:
        messagebox.showinfo("Exportar PDF", "Nenhum item para exportar.")
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        initialfile="historico_testes.pdf"
    )
    if not path:
        return
    try:
        pdf = FPDF(format="A4")
        pdf.set_margins(15, 15, 15)
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        try:
            pdf.add_font("ArialUnicode", "", "C:\\Windows\\Fonts\\arial.ttf")
            pdf.set_font("ArialUnicode", size=12)
        except Exception:
            pdf.set_font("Arial", size=12)
        from fpdf.enums import XPos, YPos
        pdf.cell(0, 10, "Histórico de Testes", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        try:
            pdf.set_font("ArialUnicode", size=9)
        except Exception:
            pdf.set_font("Arial", size=9)

        usable_width = pdf.epw

        for it in items:
            header = f"{format_timestamp(it.get('timestamp', ''))}"
            status_line = f"Status: {it.get('status','').upper()}"
            totals_line = f"Totais -> T:{it.get('total',0)}  P:{it.get('passed',0)}  F:{it.get('failed',0)}"
            grid_line = f"Plat.: {it.get('grid','')}  Vis.: {it.get('ambiente','')}  Amb.: {it.get('target_env','')}"
            nav_line = f"Nav: {it.get('navegador','')}  SO: {it.get('so','')}"
            is_mobile = it.get('ambiente', '') == 'mobile'
            device_line = (
                f"Mob.: {it.get('device','')}  Headless: {it.get('headless', False)}"
                if is_mobile else
                f"Res.: {it.get('resolution','')}  Headless: {it.get('headless', False)}"
            )
            tests_lines = []
            for name in it.get("tests_passed", []):
                tests_lines.append(f"{name} -> Passed")
            for name in it.get("tests_failed", []):
                tests_lines.append(f"{name} -> Failed")
            if not tests_lines and it.get("tests"):
                tests_lines.extend(it.get("tests"))

            for ln in (header, status_line, totals_line, grid_line, nav_line, device_line):
                pdf.multi_cell(usable_width, 6, ln, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if tests_lines:
                for tl in tests_lines:
                    pdf.multi_cell(usable_width, 6, f"- {tl}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(3)
        pdf.output(path)
        messagebox.showinfo("Exportar PDF", f"PDF salvo em:\n{path}")
    except Exception as e:
        messagebox.showerror("Exportar PDF", f"Erro ao salvar PDF:\n{e}")


def get_filtered_history():
    start_dt = build_date_from_select(
        history_start_day_var.get(),
        history_start_month_var.get(),
        history_start_year_var.get()
    )
    end_dt = build_date_from_select(
        history_end_day_var.get(),
        history_end_month_var.get(),
        history_end_year_var.get()
    )
    status_val = history_status_filter_var.get().strip().lower()
    return filter_history_items(start_dt, end_dt, status_val if status_val else "all")


def open_history_window():
    global history_window, history_rows_frame, history_empty_label
    global delete_selected_btn, delete_all_btn

    if history_window and tk.Toplevel.winfo_exists(history_window):
        history_window.deiconify()
        try:
            history_window.state("normal")
        except Exception:
            pass
        history_window.update_idletasks()
        history_window.lift()
        history_window.attributes("-topmost", True)
        history_window.after(500, lambda: history_window.attributes("-topmost", False))
        history_window.transient(app)
        history_window.focus_force()
        rebuild_history_table()
        return

    def close_history():
        global history_window
        if history_window and tk.Toplevel.winfo_exists(history_window):
            history_window.destroy()
            history_window = None

    history_window = ctk.CTkToplevel(app)
    history_window.title("Histórico de execuções")
    history_window.geometry("900x600")
    history_window.configure(fg_color=COLOR_BG)
    history_window.protocol("WM_DELETE_WINDOW", close_history)
    history_window.transient(app)
    history_window.attributes("-topmost", True)
    history_window.after(500, lambda: history_window.attributes("-topmost", False))
    history_window.grid_columnconfigure(0, weight=1)
    history_window.grid_rowconfigure(1, weight=0)
    history_window.grid_rowconfigure(2, weight=1)

    header = ctk.CTkLabel(
        history_window,
        text="Histórico de execuções",
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=18, weight="bold")
    )
    header.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

    # Filtros + export
    history_filter_frame = ctk.CTkFrame(history_window, fg_color=COLOR_PANEL, corner_radius=8)
    history_filter_frame.grid(row=1, column=0, sticky="new", padx=14, pady=(0, 8))
    history_filter_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def _date_label(day_var, month_var, year_var, default_text):
        if day_var.get() in ("DD", "") or month_var.get() in ("MM", "") or year_var.get() in ("AAAA", ""):
            return default_text
        return f"{day_var.get()}/{month_var.get()}/{year_var.get()}"

    def open_date_picker(target):
        picker = ctk.CTkToplevel(history_window)
        picker.title("Selecionar data")
        picker.geometry("280x200")
        picker.configure(fg_color=COLOR_BG)
        picker.transient(history_window)
        picker.attributes("-topmost", True)

        day_values = ["DD"] + [f"{i:02d}" for i in range(1, 32)]
        month_values = ["MM"] + [f"{i:02d}" for i in range(1, 13)]
        year_values = get_history_year_choices()

        ctk.CTkLabel(picker, text="Escolha dia/mês/ano", text_color=COLOR_TEXT).pack(pady=8)

        if target == "start":
            d_var, m_var, y_var = history_start_day_var, history_start_month_var, history_start_year_var
        else:
            d_var, m_var, y_var = history_end_day_var, history_end_month_var, history_end_year_var

        day_menu = ctk.CTkOptionMenu(picker, variable=d_var, values=day_values, fg_color=COLOR_PLACEHOLDER, button_color=COLOR_PLACEHOLDER, button_hover_color=COLOR_PLACEHOLDER, text_color=COLOR_TEXT)
        month_menu = ctk.CTkOptionMenu(picker, variable=m_var, values=month_values, fg_color=COLOR_PLACEHOLDER, button_color=COLOR_PLACEHOLDER, button_hover_color=COLOR_PLACEHOLDER, text_color=COLOR_TEXT)
        year_menu = ctk.CTkOptionMenu(picker, variable=y_var, values=year_values, fg_color=COLOR_PLACEHOLDER, button_color=COLOR_PLACEHOLDER, button_hover_color=COLOR_PLACEHOLDER, text_color=COLOR_TEXT)
        day_menu.pack(pady=4)
        month_menu.pack(pady=4)
        year_menu.pack(pady=4)

        def _confirm():
            start_label_btn.configure(text=_date_label(history_start_day_var, history_start_month_var, history_start_year_var, "Início"))
            end_label_btn.configure(text=_date_label(history_end_day_var, history_end_month_var, history_end_year_var, "Fim"))
            picker.destroy()
            on_history_filter_change()

        ctk.CTkButton(picker, text="Aplicar", command=_confirm, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER).pack(pady=8)

    def apply_today_filter():
        if today_checkbox_var.get():
            today = datetime.now().date()
            history_start_day_var.set(f"{today.day:02d}")
            history_start_month_var.set(f"{today.month:02d}")
            history_start_year_var.set(str(today.year))
            history_end_day_var.set(f"{today.day:02d}")
            history_end_month_var.set(f"{today.month:02d}")
            history_end_year_var.set(str(today.year))
        else:
            history_start_day_var.set("DD")
            history_start_month_var.set("MM")
            history_start_year_var.set("AAAA")
            history_end_day_var.set("DD")
            history_end_month_var.set("MM")
            history_end_year_var.set("AAAA")

        start_label_btn.configure(text=_date_label(history_start_day_var, history_start_month_var, history_start_year_var, "Início"))
        end_label_btn.configure(text=_date_label(history_end_day_var, history_end_month_var, history_end_year_var, "Fim"))
        on_history_filter_change()

    status_combo = ctk.CTkOptionMenu(
        history_filter_frame,
        variable=history_status_filter_var,
        values=["all", "passed", "failed"],
        fg_color=COLOR_PRIMARY,
        button_color=COLOR_PRIMARY,
        button_hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    status_combo.grid(row=0, column=0, padx=6, pady=8, sticky="ew")

    start_label_btn = ctk.CTkButton(
        history_filter_frame,
        text=_date_label(history_start_day_var, history_start_month_var, history_start_year_var, "Início"),
        command=lambda: open_date_picker("start"),
        fg_color=COLOR_CARD,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    start_label_btn.grid(row=0, column=1, padx=6, pady=8, sticky="ew")

    end_label_btn = ctk.CTkButton(
        history_filter_frame,
        text=_date_label(history_end_day_var, history_end_month_var, history_end_year_var, "Fim"),
        command=lambda: open_date_picker("end"),
        fg_color=COLOR_CARD,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    end_label_btn.grid(row=0, column=2, padx=6, pady=8, sticky="ew")

    today_checkbox = ctk.CTkCheckBox(
        history_filter_frame,
        text="Hoje",
        variable=today_checkbox_var,
        command=apply_today_filter,
        fg_color=COLOR_PRIMARY,
        hover_color=COLOR_PRIMARY_HOVER,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    today_checkbox.grid(row=0, column=3, padx=6, pady=8, sticky="e")

    delete_selected_btn = ctk.CTkButton(
        history_filter_frame,
        text="Excluir selecionados",
        command=delete_selected_history,
        state="disabled",
        fg_color=COLOR_DANGER,
        hover_color=COLOR_DANGER_HOVER,
        text_color=COLOR_TEXT
    )
    delete_selected_btn.grid(row=1, column=0, padx=6, pady=8, sticky="ew")

    delete_all_btn = ctk.CTkButton(
        history_filter_frame,
        text="Excluir todos",
        command=delete_all_history,
        fg_color=COLOR_DANGER,
        hover_color=COLOR_DANGER_HOVER,
        text_color=COLOR_TEXT
    )
    delete_all_btn.grid(row=1, column=1, padx=6, pady=8, sticky="ew")

    export_csv_btn = ctk.CTkButton(
        history_filter_frame,
        text="Exportar CSV",
        command=export_history_csv,
        fg_color=COLOR_CARD,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    export_csv_btn.grid(row=1, column=2, padx=6, pady=8, sticky="ew")

    export_pdf_btn = ctk.CTkButton(
        history_filter_frame,
        text="Exportar PDF",
        command=export_history_pdf,
        fg_color=COLOR_CARD,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    export_pdf_btn.grid(row=1, column=3, padx=6, pady=8, sticky="ew")

    history_rows_container = ctk.CTkScrollableFrame(history_window, fg_color=COLOR_PANEL, corner_radius=10)
    history_rows_container.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 14))
    history_rows_container.grid_columnconfigure(0, weight=1)

    history_empty_label = ctk.CTkLabel(
        history_rows_container,
        text="Nenhuma execução registrada ainda.",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=13)
    )
    history_empty_label.grid(row=0, column=0, padx=10, pady=10)

    history_rows_frame_local = ctk.CTkFrame(history_rows_container, fg_color="transparent")
    history_rows_frame_local.grid(row=1, column=0, sticky="nsew")
    history_rows_frame_local.grid_columnconfigure(0, weight=1)

    history_rows_frame = history_rows_frame_local
    rebuild_history_table()


def rebuild_history_table():
    global history_selection_vars

    if history_rows_frame is None or not history_rows_frame.winfo_exists():
        return

    for widget in history_rows_frame.winfo_children():
        widget.destroy()

    history_selection_vars.clear()
    items = get_filtered_history()

    if not items:
        history_empty_label.grid()
        update_delete_buttons_state()
        return
    history_empty_label.grid_remove()

    history_selection_vars = {}

    for idx, it in enumerate(items, start=1):
        row = ctk.CTkFrame(history_rows_frame, fg_color=COLOR_CARD, border_color=COLOR_BORDER, border_width=1, corner_radius=8)
        row.pack(fill="x", padx=4, pady=4)

        status_color = COLOR_SUCCESS if it.get("status") == "passed" else COLOR_DANGER
        key = it.get("id") or it.get("timestamp", f"row{idx}")
        sel_var = tk.BooleanVar(value=False)
        history_selection_vars[key] = sel_var

        header_frame = ctk.CTkFrame(row, fg_color="transparent")
        header_frame.pack(anchor="w", fill="x", padx=6, pady=(6, 2))
        select_cb = ctk.CTkCheckBox(
            header_frame,
            text="",
            variable=sel_var,
            width=18,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            border_color=COLOR_BORDER,
            command=update_delete_buttons_state
        )
        select_cb.pack(side="left", padx=(4, 6))
        header = ctk.CTkLabel(header_frame, text=f"{format_timestamp(it.get('timestamp',''))} — {it.get('status','').upper()}", text_color=status_color, font=ctk.CTkFont(size=13, weight="bold"))
        header.pack(side="left", padx=(0, 6))

        ambiente_exec = it.get("ambiente", "")
        platform_label = it.get("grid", "")
        vis_label = ambiente_exec
        target_env_label = it.get("target_env", "")
        nav_label = it.get("navegador", "")
        so_label = it.get("so", "")
        device_label = it.get("device", "") if ambiente_exec == "mobile" else ""
        res_label = it.get("resolution", "") if ambiente_exec == "desktop" else ""

        summary_text = (
            f"T:{it.get('total',0)}  P:{it.get('passed',0)}  F:{it.get('failed',0)}"
            f"   Plat.:{platform_label}  Vis.:{vis_label}  Nav:{nav_label}  SO:{so_label}"
            f"  Amb.:{target_env_label}"
            f"{f'  Mob.:{device_label}' if device_label else ''}"
            f"{f'  Res.:{res_label}' if res_label else ''}"
        )
        summary = ctk.CTkLabel(row, text=summary_text, text_color=COLOR_TEXT, font=ctk.CTkFont(size=12))
        summary.pack(anchor="w", padx=10, pady=(0, 4))
        tests_passed = it.get("tests_passed", [])
        tests_failed = it.get("tests_failed", [])
        lines = [f"{name} -> Passed" for name in tests_passed] + [f"{name} -> Failed" for name in tests_failed]
        tests_text = "\n".join(lines) if lines else "(nenhum teste registrado)"
        tests_label = ctk.CTkLabel(row, text=tests_text, text_color=COLOR_TEXT_MUTED, font=ctk.CTkFont(size=12), justify="left")
        tests_label.pack(anchor="w", padx=10, pady=(0, 6))

    update_delete_buttons_state()


# =============================================================================
# UI
# =============================================================================
def create_ui():
    global app
    global command_preview, log_box, status_label, left_selected_count_label, clear_filter_button
    global run_button, stop_button
    global total_value_label, passed_value_label, failed_value_label
    global left_tests_frame
    global test_filter_var, ambiente_var, grid_var, navegador_var, so_var, target_env_var, custom_url_var, build_name_var
    global device_var, device_choice_var, custom_device_var, custom_device_entry, device_option_menu
    global timeout_var, timeout_choice_var, timeout_option_menu
    global resolution_var, resolution_choice_var, custom_resolution_var, custom_resolution_entry, resolution_option_menu
    global headless_var
    global custom_url_label_widget, custom_url_entry_widget
    global history_rows_frame, history_status_filter_var, history_empty_label
    global history_start_day_var, history_start_month_var, history_start_year_var
    global history_end_day_var, history_end_month_var, history_end_year_var
    global today_checkbox_var
    global delete_selected_btn, delete_all_btn

    app = ctk.CTk(fg_color=COLOR_BG)
    app.title("Executor de Testes")
    app.geometry("1600x930")
    app.minsize(1300, 760)

    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    test_filter_var = tk.StringVar(value="")
    ambiente_var = tk.StringVar(value=AMBIENTE_PLACEHOLDER)
    grid_var = tk.StringVar(value=GRID_PLACEHOLDER)
    navegador_var = tk.StringVar(value=NAVEGADOR_PLACEHOLDER)
    so_var = tk.StringVar(value=SO_PLACEHOLDER)
    target_env_var = tk.StringVar(value="prod")
    custom_url_var = tk.StringVar(value="")
    default_build_name = (
        os.getenv("BS_BUILD_NAME")
        or os.getenv("LT_BUILD_NAME")
        or os.getenv("SAUCE_BUILD_NAME")
        or ""
    )
    build_name_var = tk.StringVar(value=default_build_name)
    device_choice_var = tk.StringVar(value=DEVICE_PLACEHOLDER)
    custom_device_var = tk.StringVar(value="")
    device_var = tk.StringVar(value="")
    timeout_choice_var = tk.StringVar(value=TIMEOUT_PLACEHOLDER)
    timeout_var = tk.StringVar(value="")
    resolution_choice_var = tk.StringVar(value=RESOLUTION_PLACEHOLDER)
    custom_resolution_var = tk.StringVar(value="")
    resolution_var = tk.StringVar(value="")
    headless_var = tk.BooleanVar(value=False)
    history_status_filter_var = tk.StringVar(value="all")
    today_checkbox_var = tk.BooleanVar(value=False)
    history_start_day_var = tk.StringVar(value="DD")
    history_start_month_var = tk.StringVar(value="MM")
    history_start_year_var = tk.StringVar(value="AAAA")
    history_end_day_var = tk.StringVar(value="DD")
    history_end_month_var = tk.StringVar(value="MM")
    history_end_year_var = tk.StringVar(value="AAAA")

    custom_device_var.trace_add("write", on_custom_device_change)
    custom_resolution_var.trace_add("write", on_custom_resolution_change)
    ambiente_var.trace_add("write", on_ambiente_change)
    grid_var.trace_add("write", lambda *_: on_option_placeholder_change(grid_var, GRID_PLACEHOLDER, grid_option_menu))
    navegador_var.trace_add("write", lambda *_: on_option_placeholder_change(navegador_var, NAVEGADOR_PLACEHOLDER, navegador_option_menu))
    so_var.trace_add("write", lambda *_: on_option_placeholder_change(so_var, SO_PLACEHOLDER, so_option_menu))
    timeout_choice_var.trace_add("write", lambda *_: on_option_placeholder_change(timeout_choice_var, TIMEOUT_PLACEHOLDER, timeout_option_menu))
    target_env_var.trace_add("write", on_target_env_change)
    history_status_filter_var.trace_add("write", on_history_filter_change)
    history_start_day_var.trace_add("write", on_history_filter_change)
    history_start_month_var.trace_add("write", on_history_filter_change)
    history_start_year_var.trace_add("write", on_history_filter_change)
    history_end_day_var.trace_add("write", on_history_filter_change)
    history_end_month_var.trace_add("write", on_history_filter_change)
    history_end_year_var.trace_add("write", on_history_filter_change)

    # =========================================================================
    # Coluna esquerda
    # =========================================================================
    left_panel = ctk.CTkFrame(
        app,
        width=430,
        corner_radius=0,
        fg_color=COLOR_PANEL
    )
    left_panel.grid(row=0, column=0, sticky="nsew")
    left_panel.grid_propagate(False)
    left_panel.grid_columnconfigure(0, weight=1)
    left_panel.grid_rowconfigure(4, weight=1)

    title_label = ctk.CTkLabel(
        left_panel,
        text="Selecione o(s) teste(s) abaixo:",
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=24, weight="bold")
    )
    title_label.grid(row=0, column=0, padx=20, pady=(20, 12), sticky="w")

    filter_label = ctk.CTkLabel(
        left_panel,
        text="Filtrar testes",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    filter_label.grid(row=1, column=0, padx=20, pady=(0, 4), sticky="w")

    filter_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    filter_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
    filter_frame.grid_columnconfigure(0, weight=1)

    filter_entry = ctk.CTkEntry(
        filter_frame,
        textvariable=test_filter_var,
        placeholder_text="Ex.: mobile, carrinho, checkout",
        fg_color=COLOR_INPUT,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    filter_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    filter_button = ctk.CTkButton(
        filter_frame,
        text="Filtrar",
        width=95,
        command=apply_filter,
        fg_color=COLOR_PRIMARY,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    filter_button.grid(row=0, column=1)

    clear_filter_button = ctk.CTkButton(
        filter_frame,
        text="🗑",
        width=42,
        command=clear_filter,
        fg_color=COLOR_DANGER,
        hover_color=COLOR_DANGER_HOVER,
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    clear_filter_button.grid(row=0, column=2, padx=(8, 0))
    clear_filter_button.grid_remove()

    top_actions_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    top_actions_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
    top_actions_frame.grid_columnconfigure((0, 1), weight=1)

    left_selected_count_label = ctk.CTkLabel(
        top_actions_frame,
        text="Selecionados: 0 de 0",
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=14)
    )
    left_selected_count_label.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")

    mark_all_button = ctk.CTkButton(
        top_actions_frame,
        text="Marcar todos",
        command=select_all_tests,
        fg_color=COLOR_PRIMARY,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    mark_all_button.grid(row=1, column=0, padx=(0, 5), sticky="ew")

    unmark_all_button = ctk.CTkButton(
        top_actions_frame,
        text="Desmarcar todos",
        command=deselect_all_tests,
        fg_color=COLOR_PRIMARY,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    unmark_all_button.grid(row=1, column=1, padx=(5, 0), sticky="ew")

    left_tests_frame = ctk.CTkScrollableFrame(
        left_panel,
        fg_color=COLOR_CARD,
        corner_radius=12,
        border_color=COLOR_BORDER,
        border_width=1,
        scrollbar_button_color=COLOR_SCROLL,
        scrollbar_button_hover_color=COLOR_SCROLL_HOVER
    )
    left_tests_frame.grid(row=4, column=0, padx=20, pady=(0, 12), sticky="nsew")
    left_tests_frame.grid_columnconfigure(0, weight=1)

    # =========================================================================
    # Área direita
    # =========================================================================
    right_panel = ctk.CTkFrame(
        app,
        corner_radius=0,
        fg_color=COLOR_BG
    )
    right_panel.grid(row=0, column=1, sticky="nsew")
    right_panel.grid_columnconfigure(0, weight=1)
    right_panel.grid_rowconfigure(6, weight=1)
    right_panel.grid_rowconfigure(8, weight=4)

    # Configurações
    config_frame = ctk.CTkFrame(
        right_panel,
        fg_color=COLOR_PANEL,
        corner_radius=12,
        border_color=COLOR_BORDER,
        border_width=1
    )
    config_frame.grid(row=0, column=0, padx=20, pady=(20, 12), sticky="ew")
    config_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    config_title = ctk.CTkLabel(
        config_frame,
        text="Configurações",
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    config_title.grid(row=0, column=0, columnspan=4, padx=12, pady=(12, 10), sticky="w")

    build_label = ctk.CTkLabel(
        config_frame,
        text="Build Name",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    build_label.grid(row=1, column=0, columnspan=4, padx=10, pady=(6, 4), sticky="w")

    build_entry = ctk.CTkEntry(
        config_frame,
        textvariable=build_name_var,
        fg_color=COLOR_INPUT,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT,
        placeholder_text="Ex.: Checkout Smoke 2026-03-24"
    )
    build_entry.grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 12), sticky="ew")

    ambiente_option_menu = create_labeled_option(config_frame, "Visualização", ambiente_var, [AMBIENTE_PLACEHOLDER, "desktop", "mobile"], 3, 0)
    grid_option_menu = create_labeled_option(config_frame, "Plataforma", grid_var, [GRID_PLACEHOLDER, "lt", "bs", "sauce", "local"], 3, 1)
    navegador_option_menu = create_labeled_option(config_frame, "Navegador", navegador_var, [NAVEGADOR_PLACEHOLDER, "chrome", "firefox", "edge", "safari"], 3, 2)
    so_option_menu = create_labeled_option(config_frame, "Sistema Operacional", so_var, [SO_PLACEHOLDER, "Windows 11", "Android", "iOS"], 3, 3)

    create_device_selector(config_frame, 5, 0)
    create_timeout_selector(config_frame, 5, 1)
    create_resolution_selector(config_frame, 5, 2)

    target_env_label = ctk.CTkLabel(
        config_frame,
        text="Ambiente",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    target_env_label.grid(row=9, column=0, padx=10, pady=(6, 4), sticky="w")
    target_env_menu = ctk.CTkOptionMenu(
        config_frame,
        variable=target_env_var,
        values=["prod", "stg1", "stg2", "outro"],
        fg_color=COLOR_PRIMARY,
        button_color=COLOR_PRIMARY,
        button_hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT,
        dropdown_text_color=COLOR_TEXT
    )
    target_env_menu.grid(row=10, column=0, padx=10, pady=(0, 12), sticky="ew")

    custom_url_label_widget = ctk.CTkLabel(
        config_frame,
        text="URL custom (sobrepõe ambiente)",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    custom_url_label_widget.grid(row=9, column=1, padx=10, pady=(6, 4), sticky="w")
    custom_url_entry_widget = ctk.CTkEntry(
        config_frame,
        textvariable=custom_url_var,
        fg_color=COLOR_INPUT,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT,
        placeholder_text="https://..."
    )
    custom_url_entry_widget.grid(row=10, column=1, padx=10, pady=(0, 12), sticky="ew")
    on_target_env_change()

    headless_label = ctk.CTkLabel(
        config_frame,
        text="Execução",
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14)
    )
    headless_label.grid(row=5, column=3, padx=10, pady=(4, 4), sticky="w")

    headless_checkbox = ctk.CTkCheckBox(
        config_frame,
        text="Headless",
        variable=headless_var,
        fg_color=COLOR_PRIMARY,
        hover_color=COLOR_PRIMARY_HOVER,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    headless_checkbox.grid(row=6, column=3, padx=10, pady=(6, 10), sticky="w")

    # Botões
    buttons_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
    buttons_frame.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="ew")
    buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

    stop_button = ctk.CTkButton(
        buttons_frame,
        text="Encerrar testes",
        command=stop_tests,
        state="disabled",
        height=48,
        fg_color=COLOR_DANGER,
        hover_color=COLOR_DANGER_HOVER,
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    stop_button.grid(row=0, column=0, padx=6, sticky="ew")

    run_button = ctk.CTkButton(
        buttons_frame,
        text="Executar",
        command=run_tests,
        height=48,
        fg_color=COLOR_PRIMARY,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    run_button.grid(row=0, column=1, padx=6, sticky="ew")

    preview_button = ctk.CTkButton(
        buttons_frame,
        text="Pré visualizar comando",
        command=preview_command,
        height=48,
        fg_color=COLOR_CARD,
        hover_color=COLOR_PRIMARY_HOVER,
        border_width=1,
        border_color=COLOR_PRIMARY,
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    preview_button.grid(row=0, column=2, padx=6, sticky="ew")

    # Comando
    command_header = ctk.CTkFrame(right_panel, fg_color="transparent")
    command_header.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="ew")
    command_header.grid_columnconfigure(0, weight=1)

    command_preview = ctk.CTkTextbox(
        right_panel,
        height=90,
        fg_color=COLOR_INPUT,
        border_width=1,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    command_preview.grid(row=4, column=0, padx=20, pady=(0, 12), sticky="ew")
    command_preview.insert("1.0", "A prévia do comando aparecerá aqui.")
    command_preview.configure(state="disabled")
    command_preview_visible = tk.BooleanVar(value=True)

    def toggle_command_preview():
        if command_preview_visible.get():
            command_preview.grid_remove()
            command_toggle.configure(text="Comando montado ▸")
            command_preview_visible.set(False)
        else:
            command_preview.grid()
            command_toggle.configure(text="Comando montado ▾")
            command_preview_visible.set(True)

    command_toggle = ctk.CTkButton(
        command_header,
        text="Comando montado ▾",
        command=toggle_command_preview,
        height=30,
        fg_color="transparent",
        hover_color=COLOR_CARD,
        text_color=COLOR_TEXT_MUTED,
        font=ctk.CTkFont(size=14),
        corner_radius=6,
        border_width=0
    )
    command_toggle.grid(row=0, column=0, sticky="w")

    # Status
    status_label = ctk.CTkLabel(
        right_panel,
        text="Status: aguardando execução",
        text_color=COLOR_STATUS_IDLE,
        font=ctk.CTkFont(size=18, weight="bold")
    )
    status_label.grid(row=5, column=0, padx=20, pady=(0, 12), sticky="w")

    # Resumo
    # Resumo + Logs header alinhados
    header_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
    header_frame.grid(row=6, column=0, padx=20, pady=(0, 4), sticky="ew")
    header_frame.grid_columnconfigure(0, weight=1)  # Logs label
    header_frame.grid_columnconfigure(1, weight=0)  # spacer left cards
    header_frame.grid_columnconfigure(2, weight=0)  # card1
    header_frame.grid_columnconfigure(3, weight=0)  # card2
    header_frame.grid_columnconfigure(4, weight=0)  # card3
    header_frame.grid_columnconfigure(5, weight=1)  # spacer right cards
    header_frame.grid_columnconfigure(6, weight=0)  # histórico btn

    total_value_label = create_summary_card(header_frame, "Total - 0", "", 2, "total")
    passed_value_label = create_summary_card(header_frame, "Passed - 0", "", 3, "passed")
    failed_value_label = create_summary_card(header_frame, "Failed - 0", "", 4, "failed")

    logs_label = ctk.CTkLabel(
        header_frame,
        text="Logs",
        text_color=COLOR_TEXT,
        font=ctk.CTkFont(size=15)
    )
    logs_label.grid(row=0, column=0, sticky="w")

    history_button = ctk.CTkButton(
        header_frame,
        text="Histórico",
        command=open_history_window,
        fg_color=COLOR_CARD,
        hover_color=COLOR_PRIMARY_HOVER,
        text_color=COLOR_TEXT
    )
    history_button.grid(row=0, column=6, sticky="e")

    log_box = ctk.CTkTextbox(
        right_panel,
        fg_color="#111111",
        border_width=1,
        border_color=COLOR_BORDER,
        text_color=COLOR_TEXT
    )
    log_box.grid(row=8, column=0, padx=20, pady=(0, 24), sticky="nsew")
    log_box.insert("1.0", "Os logs da execução aparecerão aqui...\n")
    log_box.configure(state="disabled")

    # Aplica regras iniciais de habilitar/desabilitar campos
    on_ambiente_change()
    on_option_placeholder_change(grid_var, GRID_PLACEHOLDER, grid_option_menu)
    on_option_placeholder_change(navegador_var, NAVEGADOR_PLACEHOLDER, navegador_option_menu)
    on_option_placeholder_change(so_var, SO_PLACEHOLDER, so_option_menu)
    on_option_placeholder_change(timeout_choice_var, TIMEOUT_PLACEHOLDER, timeout_option_menu)
    apply_menu_style(device_option_menu, device_choice_var.get() == DEVICE_PLACEHOLDER)
    apply_menu_style(resolution_option_menu, resolution_choice_var.get() == RESOLUTION_PLACEHOLDER)

    return app


def on_target_env_change(*_args):
    show_custom = (target_env_var.get() or "").strip().lower() == "outro"
    if custom_url_label_widget and custom_url_entry_widget:
        if show_custom:
            custom_url_label_widget.grid()
            custom_url_entry_widget.grid()
            custom_url_entry_widget.configure(state="normal")
        else:
            custom_url_var.set("")
            custom_url_label_widget.grid_remove()
            custom_url_entry_widget.grid_remove()


# =============================================================================
# Inicialização
# =============================================================================
def load_tests():
    global all_test_files
    all_test_files = discover_tests()
    rebuild_left_tests()


def main():
    load_history()
    create_ui()
    load_tests()
    rebuild_history_table()
    poll_log_queue()
    app.mainloop()


if __name__ == "__main__":
    main()

