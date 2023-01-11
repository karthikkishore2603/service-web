from . import models
from jinja2 import Environment
from weasyprint import HTML
import io
import os


env = Environment()


LAYOUT = """
<head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
        <title>SERVICE WEB</title>
        
        
</head>
<script src="https://kit.fontawesome.com/623b0bceda.js" crossorigin="anonymous"></script>

<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet"> 
    <title>Report</title>
    <style>
        * {
            margin-left: auto;
            margin-right: auto;
            border-collapse: collapse;
            width: auto;
            
        }

        table,
        th,
        td {
            font-family: 'Open Sans', sans-serif;
            font-size: 15px;
            border-color: black;
            border-collapse: collapse;
            border-style: solid;
            padding: 5px;
        }
    </style>

</head>

<body>


   
<h1 style="font-family: sans;text-align: center;">COM CARE SERVICES</h1>
    <h3 style="font-family: sans;text-align: center;">Service  Recipt</h3>
    <br>
    <div class="row" >
        <div class="col" >
          <h3 style="font-family: 'Times New Roman', serif; ">Task ID</label>
        </div>
        <div class="col">
          <h3 style="font-family:  Tahoma, sans-serif;">{{ tasks.task_id }}</h3>
        </div>
        <div class="col">
          <h3 style="font-family: 'Times New Roman', serif; ">Date</h3>
        </div>
        <div class="col">
          <h3 style="font-family:  Tahoma, sans-serif;">{{ tasks.date }}</h3>
        </div>
        
      </div>   
    
        <div class="row">
            
            <div class="col">
              <h3 style="font-family: 'Times New Roman', serif; ">Customer Name</h3>
            </div>
            <div class="col">
              <h3 style="font-family:  Tahoma, sans-serif;">{{ tasks.customer.name }}</h3>
            </div>
            <div class="col">
              <h3 style="font-family: 'Times New Roman', serif; ">Phone No</h3>
            </div>
            <div class="col">
              <h3 style="font-family:  Tahoma, sans-serif;">{{ tasks.customer.phone_no }}</h3>
            </div>
          </div>
    
          <div class="row">
            
            <div class="col">
              <h3 style="font-family: 'Times New Roman', serif; ">Engineer</h3>
            </div>
            <div class="col">
              <h3 style="font-family:  Tahoma, sans-serif;">{{ tasks.technician.name }}</h3>
            </div>
            <div class="col">
              <h3 style="font-family: 'Times New Roman', serif; ">Engineer</h3>
            </div>
            <div class="col">
              <h3 style="font-family:  Tahoma, sans-serif;">{{ tasks.technician2.name }}</h3>
            </div>
          </div>

          <div class="row">
            
            <div class="col">
              <h3 style="font-family: 'Times New Roman', serif; ">Service Charges</h3>
            </div>
            <div class="col">
              <h3 style="font-family:  Tahoma, sans-serif;">{{ resources.service_charge }}</h3>
            </div>
            <div class="col">
              <h3 style="font-family: 'Times New Roman', serif; ">Received Charge</h3>
            </div>
            <div class="col">
              <h3 style="font-family:  Tahoma, sans-serif;">{{ resources.received_charge }}</h3>
            </div>
          </div>
    <br>

            <div class="row">
            
            <div class="col">
              <h3 style="font-family: 'Times New Roman', serif; ">Materials</h3>
            </div>
            <div class="col">
              <h3 style="font-family:  Tahoma, sans-serif;">{{ resources.material }}</h3>
            </div>
            <div class="col">
              
            <div class="col">
              
            </div>
          </div>
</body>
"""

LAYOUT1 = """
<head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
        <title>SERVICE WEB</title>
        
        
</head>
<script src="https://kit.fontawesome.com/623b0bceda.js" crossorigin="anonymous"></script>

<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet"> 
    <title>Report</title>
    <style>
        * {
            margin-left: auto;
            margin-right: auto;
            border-collapse: collapse;
            width: auto;
            
        }

        table,
        th,
        td {
            font-family: 'Open Sans', sans-serif;
            font-size: 15px;
            border-color: black;
            border-collapse: collapse;
            border-style: solid;
            padding: 5px;
        }
    </style>

</head>

<body>


   
<h1 style="font-family: sans;text-align: center;">COM CARE SERVICES</h1>
    <h3 style="font-family: sans;text-align: center;">Service  Recipt</h3>
    <br>
    <div class="table-responsive">
            <br>
            <h2 class="h3">Work</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">OS.ID</th>
                        <th scope="col">Date</th>
                        <th scope="col">Customer Name</th>
                        <th scope="col">Status</th>
                        <th scope="col">View</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    {% for task in tasks -%}
                    <tr>
                        <td>
                            {{ task.task_id }}
                        </td>
                        <td>
                            <p>{{ task.date }}</p>
                        </td>
                        <td>
                            <p>{{ task.customer.name }}</p>
                        </td>
                        <td>
                            <p>{{ task.technician.technician_id }}</p>
                        </td>



                        
                    </tr>

                    {% endfor -%}
                </tbody>
            </table>

        </div> 

</body>
"""
def create_html(tasks : models.OnsiteTask , resources: models.Resources) -> str:
    template = env.from_string(LAYOUT)
    html = template.render(tasks=tasks ,resources=resources)
    print (html)
    return html


def create_pdf(tasks : models.OnsiteTask, resources: models.Resources) -> io.BytesIO:
    html = create_html(tasks=tasks,resources=resources)
    return io.BytesIO(HTML(string=html).write_pdf())


def create_customer_report_html(tasks : models.OnsiteTask ) -> str:
    template = env.from_string(LAYOUT)
    html = template.render(tasks=tasks ,resources=resources)
    print (html)
    return html

def create_customer_work_pdf(tasks : models.OnsiteTask) -> io.BytesIO:
    html = create_customer_report_html(tasks=tasks)
    return io.BytesIO(HTML(string=html).write_pdf())