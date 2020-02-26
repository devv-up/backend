# DEV-UP

## 콘다 env 설정
```bash
conda env create -f conda.yaml 
```

## VSCode 설정
`.vscode` 폴더안에 `settings.json` 안에 다음과 같은 내용을 써주세요
이미 내용이 있다면 추가시키세요
```javascript
{
    "[python]": {
        "editor.formatOnSave": true,
        "editor.formatOnPaste": false,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "python.linting.mypyEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.jediEnabled": false
}
```
