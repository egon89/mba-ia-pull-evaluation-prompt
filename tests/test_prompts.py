"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_NAME = "bug_to_user_story_v2"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_prompt_data() -> dict:
    """Carrega e retorna apenas o prompt alvo do arquivo YAML."""
    prompts = load_prompts(PROMPT_FILE)
    return prompts[PROMPT_NAME]

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt_data = get_prompt_data()
        assert prompt_data.get("system_prompt", "").strip()

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt_data = get_prompt_data()
        system_prompt = prompt_data["system_prompt"]
        assert "Você é um Product Manager" in system_prompt or "Product Manager Sênior" in system_prompt

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt_data = get_prompt_data()
        system_prompt = prompt_data["system_prompt"]
        assert "## User Story" in system_prompt
        assert "## Critérios de Aceitação" in system_prompt
        assert "## Edge Cases" in system_prompt

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt_data = get_prompt_data()
        system_prompt = prompt_data["system_prompt"]
        assert system_prompt.count("EXEMPLO") >= 3
        assert "Entrada:" in system_prompt
        assert "Saída:" in system_prompt

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt_data = get_prompt_data()
        assert "TODO" not in prompt_data["system_prompt"]
        assert "TODO" not in prompt_data.get("user_prompt", "")

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt_data = get_prompt_data()
        is_valid, errors = validate_prompt_structure(prompt_data)
        assert is_valid, errors
        assert len(prompt_data.get("techniques_applied", [])) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])