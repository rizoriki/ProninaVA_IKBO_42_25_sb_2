"""NuGet package dependency parser."""
import io
import json
import urllib.request
import zipfile

NUGET_API_URL = "https://api.nuget.org/v3-flatcontainer"

def get_direct_dependencies(package):
    """Get direct dependencies of NuGet package."""
    url = f"{NUGET_API_URL}/{package}/index.json"
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
            versions = data.get("versions", [])
            if not versions:
                return []
            latest = versions[-1]
            return _download_nuspec(package, latest)
    except Exception as err:
        raise RuntimeError(f"Failed to fetch: {err}") from err

def _download_nuspec(package, version):
    """Download and parse nuspec from nupkg."""
    filename = f"{package}.{version}.nupkg"
    url = f"{NUGET_API_URL}/{package}/{version}/{filename}"
    with urllib.request.urlopen(url) as resp:
        nupkg_data = resp.read()
    
    with zipfile.ZipFile(io.BytesIO(nupkg_data)) as arc:
        for name in arc.namelist():
            if name.endswith(".nuspec"):
                content = arc.read(name).decode("utf-8")
                return _parse_nuspec(content)
    return []

def _parse_nuspec(xml_content):
    """Parse nuspec XML to extract dependencies."""
    deps = []
    in_deps = False
    for line in xml_content.split("\n"):
        if "<dependencies" in line:
            in_deps = True
            continue
        if "</dependencies>" in line:
            in_deps = False
            continue
        if in_deps and "<dependency" in line:
            start = line.find('id="')
            if start != -1:
                start += 4
                end = line.find('"', start)
                if end != -1:
                    deps.append(line[start:end])
    return deps
