In aceasta documentatie, comparatia este facuta intre doua etape ale suitei de teste:

| Etapa | Descriere |
| --- | --- |
| Suita initiala | Prima varianta de teste, construita pentru validarea functionalitatilor principale: username, email, parola, varsta, termeni si validarea completa a inregistrarii |
| Suita imbunatatita cu asistenta AI | Varianta obtinuta dupa analizarea mutantilor supravietuitori si adaugarea unor teste suplimentare pentru comportamente care nu erau verificate suficient |

### Modul de folosire a ChatGPT

ChatGPT a fost folosit pentru:

- explicarea rezultatelor obtinute cu `pytest`, `coverage` si `mutmut`;
- suport in rularea comenzilor si activarea `mutmut`;
- identificarea diferentelor dintre coverage si mutation testing;
- analizarea mutantilor supravietuitori;
- propunerea unor teste suplimentare;
- explicarea motivului pentru care anumiti mutanti au supravietuit;

### Exemple de prompturi folosite

**Prompt 1:**

> Am rulat mutmut si am mutanti survived. Cum pot analiza acesti mutanti si ce teste suplimentare ar trebui sa adaug?

**Prompt 2:**

> Mutantul modifica mesajul de eroare pentru username/email, dar testele tot trec. Ce inseamna asta si cum il pot omori cu un test?

### Exemple de imbunatatiri propuse

Dupa analiza mutantilor, au fost adaugate teste pentru:

- toate parolele comune din `DEFAULT_COMMON_PASSWORDS`;
- verificarea faptului ca litera `X` nu este considerata caracter special;
- mesajul exact pentru username prea scurt;
- mesajul exact pentru username prea lung;
- mesajul exact pentru username cu format invalid;
- mesajul exact pentru email cu spatii.

### Comparatie rezultate

| Etapa | Rezultat pytest | Mutanti killed | Mutanti survived | Interpretare |
| --- | --- | --- | --- | --- |
| Suita initiala | 58 de teste treceau | 100 | 36 | Testele acopereau functionalitatile principale, dar unii mutanti au supravietuit |
| Dupa prima imbunatatire | 73 de teste treceau | 113 | 22 | Au fost imbunatatite testele pentru parole comune si caractere speciale |
| Dupa a doua imbunatatire | 77 teste treceau | 119 | 17 | Au fost adaugate teste mai stricte pentru mesajele de eroare |

### Interpretare

Folosirea ChatGPT a fost utila mai ales in etapa de analiza a mutantilor supravietuitori. Raportul de coverage indica 100% acoperire pentru fisierul principal, dar `mutmut` a aratat ca anumite comportamente nu erau verificate suficient de strict.

Prin adaugarea testelor suplimentare, numarul de mutanti omorati a crescut de la 100 la 119, iar numarul de mutanti supravietuitori a scazut de la 36 la 17.

ChatGPT a fost folosit pentru generarea de cod functional, repararea greselilor/erorilor, interpretarea rezultatelor si imbunatatirea calitatii suitei de testare.

### Capturi de ecran

Capturile relevante pentru aceasta sectiune au in nume GPT si se afla in folderul:

`docs/screenshots/`