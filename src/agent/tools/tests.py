import pytest

from langchain_core.messages import AIMessage
from langchain_core.exceptions import OutputParserException
from unittest.mock import patch
from .scene import SceneAnalyzer
from .decomposer import Decomposer
from .improver import Improver


class TestImprover:
    @pytest.fixture
    def improver(self):
        return Improver()

    @pytest.fixture
    def sample_prompt(self):
        return "Generate a Japanese theatre scene with samurai armor in the center"

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_improve(self, mock_llm_invoke, improver, sample_prompt):
        mock_response = "Generate a traditional Japanese theatre scene with Samurai armor placed in the center of the stage. The room should have wooden flooring, simple red and gold accents, and folding screens in the background. The Samurai armor should be detailed, with elements like the kabuto (helmet) and yoroi (body armor), capturing the essence of a classical Japanese theatre setting."
        mock_llm_invoke.return_value = AIMessage(content=mock_response)

        result = improver.improve(sample_prompt)

        assert result == mock_response
        mock_llm_invoke.assert_called_once()

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_improve_llm_api_error(self, mock_llm_invoke, improver, sample_prompt):
        error_message = "Ollama service unreachable"
        mock_llm_invoke.side_effect = ConnectionError(error_message)

        with pytest.raises(ConnectionError, match=error_message):
            improver.improve(sample_prompt)

        mock_llm_invoke.assert_called_once()


class TestDecomposer:
    @pytest.fixture
    def decomposer(self):
        return Decomposer()

    @pytest.fixture
    def sample_prompt(self):
        return "Generate a traditional Japanese theatre room with intricate wooden flooring, high wooden ceiling beams, elegant red and gold accents, and large silk curtains."

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_decompose(self, mock_llm_invoke, decomposer, sample_prompt):
        mock_response = '{"scene": {"objects": [{"name": "theatre_room", "type": "room", "position": {"x": 0, "y": 0, "z": 0}, "rotation": {"x": 0, "y": 0, "z": 0}, "scale": {"x": 20, "y": 10, "z": 20}, "material": "traditional_wood_material", "prompt": "Generate an image of a squared traditional Japanese theatre room viewed from the outside at a 3/4 top-down perspective."}]}}'
        mock_llm_invoke.return_value = AIMessage(content=mock_response)

        result = decomposer.decompose(sample_prompt)

        expected = {
            "scene": {
                "objects": [
                    {
                        "name": "theatre_room",
                        "type": "room",
                        "position": {"x": 0, "y": 0, "z": 0},
                        "rotation": {"x": 0, "y": 0, "z": 0},
                        "scale": {"x": 20, "y": 10, "z": 20},
                        "material": "traditional_wood_material",
                        "prompt": (
                            "Generate an image of a squared traditional Japanese theatre room "
                            "viewed from the outside at a 3/4 top-down perspective."
                        ),
                    }
                ]
            }
        }
        assert result == expected
        mock_llm_invoke.assert_called_once()

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_invalid_json_response(self, mock_llm_invoke, decomposer):
        mock_llm_invoke.return_value = AIMessage(content='{"scene": [invalidjson]}')

        user_input = "Blablabla"
        with pytest.raises(OutputParserException) as e:
            decomposer.decompose(user_input)

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_decompose_llm_api_error(self, mock_llm_invoke, decomposer, sample_prompt):
        error_message = "Ollama service unreachable"
        mock_llm_invoke.side_effect = ConnectionError(error_message)

        with pytest.raises(ConnectionError, match=error_message):
            decomposer.decompose(sample_prompt)

        mock_llm_invoke.assert_called_once()


class TestSceneAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return SceneAnalyzer()

    @pytest.fixture
    def sample_scene(self):
        return {
            "objects": [
                {"name": "table", "position": [0, 0, 0]},
                {"name": "chair", "position": [1, 0, 1]},
                {"name": "lamp", "position": [0, 1, 0], "state": "off"},
            ],
            "lights": [{"id": "main", "intensity": 0.8}],
        }

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_one_element_selection(self, mock_llm_invoke, analyzer, sample_scene):
        mock_response = '{"objects": [{"name": "table", "position": [0, 0, 0]}]}'
        mock_llm_invoke.return_value = AIMessage(content=mock_response)

        user_input = "Add a vase on the table"
        result = analyzer.analyze(sample_scene, user_input)

        expected = {"objects": [{"name": "table", "position": [0, 0, 0]}]}
        assert result == expected

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_multiple_elements_selection(self, mock_llm_invoke, analyzer, sample_scene):
        mock_response = '{"objects": [{"name": "lamp", "position": [0, 1, 0], "state": "off"}], "lights": [{"id": "main", "intensity": 0.8}]}'
        mock_llm_invoke.return_value = AIMessage(content=mock_response)

        user_input = "Turn on the lamp and adjust main light"
        result = analyzer.analyze(sample_scene, user_input)

        expected = {
            "objects": [{"name": "lamp", "position": [0, 1, 0], "state": "off"}],
            "lights": [{"id": "main", "intensity": 0.8}],
        }
        assert result == expected
        mock_llm_invoke.assert_called_once()

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_invalid_json_response(self, mock_llm_invoke, analyzer, sample_scene):
        mock_llm_invoke.return_value = AIMessage(content='{"objects": [invalidjson]}')

        user_input = "Blablabla"
        with pytest.raises(OutputParserException) as e:
            analyzer.analyze(sample_scene, user_input)

        mock_llm_invoke.assert_called_once()

    @patch("langchain_ollama.llms.OllamaLLM.invoke")
    def test_analyze_llm_api_error(self, mock_llm_invoke, analyzer, sample_scene):
        error_message = "Ollama service unreachable"
        mock_llm_invoke.side_effect = ConnectionError(error_message)

        user_input = "Whatever"
        with pytest.raises(ConnectionError, match=error_message):
            analyzer.analyze(sample_scene, user_input)

        mock_llm_invoke.assert_called_once()
