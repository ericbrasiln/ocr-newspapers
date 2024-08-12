# ocr-newspapers

Repositório com *scripts* para extrair textos de pdfs de jornais digitalzados.

## Uso

Para usar o script, basta rodar o comando abaixo:

```bash
python3 ocr-np.py <caminho para o diretório com os pdfs> <caminho para o diretório de saída>
```

### Exemplo

```bash
python3 ocr-np.py ./pdf_test/ ./txt_test/
```
Veja os arquivos de exemplo na pasta `pdf_test/` e os resultados na pasta `txt_test/`.

## Dependências

- Python 3
- pytesseract
- pdf2image

## Licença

MIT

