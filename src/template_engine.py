"""Simple template engine that wires logic blocks into structured pages."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class TemplateField:
    name: str
    resolver: Callable[[Dict[str, Any]], Any]


@dataclass
class Template:
    name: str
    fields: List[TemplateField] = field(default_factory=list)


class TemplateRegistry:
    def __init__(self) -> None:
        self._templates: Dict[str, Template] = {}

    def register(self, template: Template) -> None:
        self._templates[template.name] = template

    def get(self, name: str) -> Template:
        if name not in self._templates:
            raise KeyError(f"Template '{name}' is not registered")
        return self._templates[name]


class TemplateEngine:
    def __init__(self, registry: TemplateRegistry) -> None:
        self.registry = registry

    def render(self, template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        template = self.registry.get(template_name)
        rendered: Dict[str, Any] = {"template": template.name}
        for field in template.fields:
            rendered[field.name] = field.resolver(context)
        return rendered


