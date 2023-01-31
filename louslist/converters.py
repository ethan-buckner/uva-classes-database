def to_python(value):
    return int(value)
class DepartmentConverter:
     regex = '[a-z]{2,4}'

     def to_python(self, value):
         return int(value)


     def to_url(self, value):
         return str(value)