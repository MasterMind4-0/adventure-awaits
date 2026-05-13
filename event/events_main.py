import importlib.util
from pathlib import Path

eventsdict = {}
eventsls = []
events_dir = Path('event/events')

for path in events_dir.glob('*.py'):
    if path.name == '__init__.py':
        continue
    stem = path.stem
    spec = importlib.util.spec_from_file_location(stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    func = getattr(mod, stem)
    tags = getattr(mod, 'tags', {})
    eventsdict[stem] = {'name': stem, 'call': func, 'tags': tags}

for event in eventsdict.keys():
    eventsls.append(eventsdict[event]['call'])