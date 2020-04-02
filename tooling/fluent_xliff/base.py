import os
import xml.etree.ElementTree as ET
from compare_locales.paths import ProjectFiles
from fluent.syntax import ast, parse, serializer

xmlns = "urn:oasis:names:tc:xliff:document:2.0"
ET.register_namespace("", xmlns)


class XLIFFer:
    def __init__(self, config):
        self.config = config

    @property
    def locales(self):
        return self.config.all_locales

    def xliff(self, locale):
        files = ProjectFiles(locale, [self.config])
        root = ET.Element(
            f"{{{xmlns}}}xliff", {"version": "2.0", "srcLang": "en", "trgLang": locale,}
        )
        root.text = "\n  "
        root.tail = "\n"
        previous = None
        for l10n, ref, _, _ in files:
            if previous is not None:
                previous.tail += "  "
            ref_id = os.path.relpath(ref, self.config.root)
            ref_id = ref_id.replace("/", "-")
            file_elem = ET.SubElement(root, f"{{{xmlns}}}file", {"id": ref_id})
            file_elem.tail = "\n"
            file_elem.text = "\n  "
            self.file(file_elem, ref, l10n, locale)
            previous = file_elem
        ET.dump(root)

    def file(self, parent, ref, l10n, locale):
        if not os.path.isfile(ref):
            return
        with open(ref) as fh:
            ref_entries = parse(fh.read(), with_spans=False).body
        l10n_entries = {}
        if os.path.isfile(l10n):
            with open(l10n) as fh:
                l10n_entries = {
                    ("-" if isinstance(e, ast.Term) else "") + e.id.name: e
                    for e in parse(fh.read(), with_spans=False).body
                    if isinstance(e, (ast.Message, ast.Term))
                }
        root = parent
        indent = 1
        group_id = 1
        for entry in ref_entries:
            if isinstance(entry, ast.GroupComment):
                parent = root
                if not entry.content:
                    continue
                parent = ET.SubElement(
                    parent, f"{{{xmlns}}}group", {"id": f"group-{group_id}"}
                )
                group_id += 1
                parent.text = "\n    "
                parent.tail = "\n  "
                notes = ET.SubElement(parent, f"{{{xmlns}}}notes")
                notes.tail = "\n  "
                note = ET.SubElement(notes, f"{{{xmlns}}}note")
                note.text = entry.content
            elif isinstance(entry, (ast.Message, ast.Term)):
                entry_id = "-" if isinstance(entry, ast.Term) else ""
                entry_id += entry.id.name
                unit = ET.SubElement(parent, f"{{{xmlns}}}unit", {"id": entry_id})
                unit.text = "\n" + (indent + 1) * "  "
                unit.tail = "\n" + indent * "  "
                if entry.comment:
                    notes = ET.SubElement(unit, f"{{{xmlns}}}notes")
                    notes.tail = "\n" + (indent + 1) * "  "
                    note = ET.SubElement(notes, f"{{{xmlns}}}note")
                    note.text = entry.comment.content
                segment = ET.SubElement(unit, f"{{{xmlns}}}segment")
                segment.tail = segment.text = "\n" + (indent + 1) * "  "
                source = ET.SubElement(segment, f"{{{xmlns}}}source")
                source.tail = "\n" + (indent + 1) * "  "
                content = serializer.serialize_pattern(entry.value)
                # serialize_pattern prefixes inline patterns with " ", which we don't want
                if content[0] == " ":
                    content = content[1:]
                source.text = content
                if entry_id not in l10n_entries:
                    continue
                target = ET.SubElement(segment, f"{{{xmlns}}}target")
                target.tail = "\n" + (indent + 1) * "  "
                content = serializer.serialize_pattern(l10n_entries[entry_id].value)
                # serialize_pattern prefixes inline patterns with " ", which we don't want
                if content[0] == " ":
                    content = content[1:]
                target.text = content
