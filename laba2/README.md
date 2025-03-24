## Подготовка

Сделайте файл исполняемым:
```
chmod +x greeting.py
```

### Ввод из файла

Заполним файл `names.txt`:
```
Ivan
Elizaveta
konstantin
__Maxim__
Kir4
Daniel Alina
```
Выполним команду.
```
./greeting.py < names.txt 2> error.txt
```

Вывод в терминал:
```
Hello, Ivan! Nice to see you!
Hello, Elizaveta! Nice to see you!
Hello, Daniel! Nice to see you!
Hello, Alina! Nice to see you!
```

Вывод в `error.txt`:
```
Error: 'konstantin' is not a valid name.
Error: '__Maxim__' is not a valid name.
Error: 'Kir4' is not a valid name.
```


### Интерактивный режим
Выполним команду:
```
./greeting.py
```

Пример работы:
```
Enter your name: Ivan 
Hello, Ivan! Nice to see you!
Enter your name: Ivan182
Error: 'Ivan182' is not a valid name.
Enter your name: __ivan__
Error: '__ivan__' is not a valid name.
Enter your name:
Goodbye!
```
Чтобы завершить программу используйте `Ctrl + C`.


