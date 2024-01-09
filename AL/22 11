using System;

class Student{
    
    public static void FindByName(Student st, string name){
        if(st.Name == name){
            Console.WriteLine(st);
        }
    }
    
    public static void FindByYearOfBirth(Student st, string yearOfBirth){
        if(st.YearOfBirth == yearOfBirth){
            Console.WriteLine(st);
        }
    }
    
    public static void FindByGroup(Student st, string group){
        if(st.Group == group){
            Console.WriteLine(st);
        }
    }
    
    public string Name {get; set;}
    public string YearOfBirth {get; set;}
    public string Group {get; set;}
    
    public Student(){
        this.Name = "Иванов Иван Иванович";
        this.YearOfBirth = "01.01.1999";
        this.Group = "ФИТ-231";
    }
    
    public override string ToString(){
        return $"Имя: {Name} \nГод рождения: {YearOfBirth} \nГруппа: {Group}";
    }
}

class HelloWorld {
  static void Main() {
    Student[] sts = new Student[10];
    for(int i = 0; i < sts.Length; i++){
        sts[i] = new Student();
        
        sts[i].Name = "Студент номер " + (i+1);
        sts[i].YearOfBirth = "01.01.199" + i;
        sts[i].Group = "ФИТ-23" + i;
    }
    
    Console.WriteLine("Выберите тип фильтра (1 - ФИО, 2 - Год рождения, 3 - Группа):");
    string filterType = Console.ReadLine();
    if(filterType == "1"){
        Console.Write("Введите ФИО студента: ");
        string name = Console.ReadLine();
        foreach(Student i in sts){
            Student.FindByName(i, name);
        }
    } else if(filterType == "2"){
        Console.Write("Введите год рождения студента: ");
        string yearOfBirth = Console.ReadLine();
        foreach(Student i in sts){
            Student.FindByYearOfBirth(i, yearOfBirth);
        }
    } else if(filterType == "3"){
        Console.Write("Введите группу студента: ");
        string group = Console.ReadLine();
        foreach(Student i in sts){
            Student.FindByGroup(i, group);
        }
    } else {
        Console.Write("Недопустимый ввод");
    }
  }
}
