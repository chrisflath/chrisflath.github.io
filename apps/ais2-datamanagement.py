import marimo

__generated_with = "0.13.4"
app = marimo.App(
    width="medium",
    app_title="Data Management",
    layout_file="layouts/ais2-datamanagement.slides.json",
    css_file="d3.css",
)


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from io import StringIO
    return StringIO, mo, pd


@app.cell
def _(mo):
    class Slide:
        def __init__(self, title, slide_number, chair_title="Default Chair Title", lecture_name="Default Lecture Name", layout_type="2-column", presenter="Default Presenter", section="Default Section"):  
            self.slide_data = {}
            self.section = section
            self.layout_type = layout_type
            self.lecture_name = lecture_name
            self.presenter = presenter
            self.title = title
            self.title_raw = title
            self.content1 = mo.md("")
            self.content2 = mo.md("")
            self.chair_title = chair_title
            self.slide_number = slide_number
            self.vertical_spacer_height = 800
            self.horizontal_spacer_width = 1280
            self.logo = mo.image("https://raw.githubusercontent.com/d3group/.github/refs/heads/main/assets/D3_2c.png", width=200)

        def get_spacer_horizontal(self, size=1200):
            return mo.md(r"""&nbsp;""").style({"width": f"{size}px"})

        def get_spacer_vertical(self, size=600):
            return mo.md(r"""&nbsp;""").style({"height": f"{size}px"})

        def get_horizontal_rule(self):
            return mo.md(f"<div style='width: {self.horizontal_spacer_width}px; height: 1px; background-color: darkgray;'></div>")

        def get_footer(self, slide_number=0):
            if slide_number is not None:
                return mo.vstack([
                    self.get_horizontal_rule(),
                    mo.hstack([
                        mo.hstack([mo.md(f"Page {slide_number}  |  "),
                        mo.md(f"_{self.chair_title}_  | "), mo.md(f" _{self.lecture_name}_")], gap=0, justify="start"),
                        mo.vstack([self.logo], gap=0, align="end")
                    ], widths=[0.8,0.2])
                ], align="start")
            else:
                return mo.vstack([
                    self.get_horizontal_rule(),
                    mo.hstack([
                            mo.hstack([mo.md("Agenda | "),
                            mo.md(f"_{self.chair_title}_ | "), mo.md(f"_{self.lecture_name}_")], gap=0, justify="start"),
                        mo.vstack([self.logo], gap=0, align="end")
                    ], widths=[0.8,0.2])
                ], align="start")

        def render_slide(self, left_width=750, right_width=450, content1=None, content2=None):
            title_style = {"width": "100%", "text-align": "left"}  # Ensure full width and left alignment

            if self.title != "Agenda":
                title_content = mo.vstack([
                    mo.md(f"<span style='font-size: 90%; color: gray;'>_{self.section}_</span>"),
                    mo.md(f"# {self.title}").style(title_style)
                ], align="start")
            else:
                title_content = mo.vstack([
                    mo.md(f"<span style='font-size: 90%; color: gray;'>_ _</span>"),
                    mo.md(f"# {self.title}").style(title_style)
                ], align="start")

            # Generic slide structure
            def create_slide_content(content, include_footer=True):
                elements = [
                    self.get_spacer_horizontal(),
                    title_content,
                    self.get_horizontal_rule(),
                    content
                ]
                if include_footer:
                    elements.append(self.get_footer(self.slide_number))
                return mo.vstack(elements, gap=0, justify="start", align="start")

            if self.layout_type == "title-slide":
                self.section = None
                content = mo.hstack([self.get_spacer_vertical(),mo.vstack([
                    self.get_spacer_horizontal(),
                    self.get_spacer_vertical(100),
                    mo.hstack([
                        mo.md("""<div style='width: 4px; height: 300px; background-color: darkgray;'></div>"""),
                        mo.vstack([mo.md(f"<span style='font-size:2em;'>{self.lecture_name}</span>"),
                                   mo.md(f"#{self.title_raw}"),
                                   mo.md(""),
                                   mo.md(""),
                        mo.hstack([
                        mo.vstack([
                            mo.md(f"{self.presenter} ({self.chair_title})")
                        ], align="start"),

                        self.content2],align="center", gap=1, justify="space-around")], align="start")
                    ], justify="start", align="start", gap=5).style({"text-align": "left"}),
                    self.get_spacer_vertical(100),
                ], gap=0, justify="start")])
                slide = mo.vstack([content,mo.vstack([self.logo], gap=0, align="end")], gap=0)

            elif self.layout_type == "1-column":
                content = mo.hstack([
                    self.get_spacer_vertical(),
                    self.content1.style({"width": "100%"})
                ], gap=0, justify="center", align="center")
                slide = create_slide_content(content)

            elif self.layout_type == "side-by-side":
                content = mo.hstack([
                    self.get_spacer_vertical(),
                    self.content1.style({"width": "600px", "margin-left": "auto", "margin-right": "auto"}),
                    self.content2.style({"width": "600px", "margin-left": "auto", "margin-right": "auto"}),
                ], gap=0, justify="center", align="center")
                slide = create_slide_content(content)

            elif self.layout_type == "flexible-2-column":
                content = mo.hstack([
                    self.get_spacer_vertical(),
                    self.content1.style({"width": f"{left_width}px", "margin-left": "auto", "margin-right": "auto"}),
                    self.content2.style({"width": f"{right_width}px", "margin-left": "auto", "margin-right": "auto"}),
                ], gap=0, justify="center", align="center")
                slide = create_slide_content(content)

            else:  # Default layout
                content = mo.hstack([
                    self.get_spacer_vertical(),
                    self.content1.style({"width": "750px", "margin-left": "auto", "margin-right": "auto"}),
                    self.content2.style({"width": "450px", "margin-left": "auto", "margin-right": "auto"}),
                ], gap=0, justify="center", align="center")
                slide = create_slide_content(content)

            slide = mo.vstack([slide, mo.Html("""<div class="page-break"></div>""")])
            return slide

        def get_title_number(self):
            return (self.title_raw, self.slide_number)

    class SlideCreator:
        def __init__(self, chair_title="Default Chair Title", lecture_name="Default Lecture Name", presenter="Default Presenter"):
            self.chair_title = chair_title
            self.lecture_name = lecture_name
            self.presenter = presenter
            self.pages = []
            self.currentSection = "Default Section"


        def create_slide(self, title, layout_type="2-column", newSection=None):
            if newSection:
                self.currentSection = newSection
            slide = Slide(title, len(self.pages)+1, chair_title=self.chair_title, lecture_name=self.lecture_name, presenter=self.presenter, layout_type=layout_type, section=self.currentSection)
            self.pages.append(slide)
            return slide

        def create_agenda(self, title="Agenda", currentSection=None):
            agenda = {}
            for page in self.pages:
                if page.section is not None:
                    if page.section not in agenda:
                        agenda[page.section] = []
                    agenda[page.section].append(page.get_title_number()[0])

            # Creating a slide similar to the title-slide layout
            agenda_slide = Slide(title, None, chair_title=self.chair_title,
                                lecture_name=self.lecture_name, presenter=self.presenter,
                                layout_type="1-column", section=currentSection or self.currentSection)

            # Building the markdown content for agenda
            agenda_content = ""
            for section, titles in agenda.items():
                if currentSection is not None and section == currentSection:
                    agenda_content += f"<span style='background-color:lightblue; font-weight:bold; color:gray; display: inline-block; width: 450px;'>{section}</span>\n\n"
                else:
                    agenda_content += f"**{section}**\n\n"
                # if currentSection is not None and section == currentSection:
                #     for slide_title in titles:
                #         agenda_content += f"\n &nbsp;&nbsp; <sub>{slide_title}</sub> \n"
                # agenda_content += "\n \n"

            # Setting the content of the slide
            agenda_slide.content1 = mo.md(agenda_content)

            self.pages.append(agenda_slide)
            return agenda_slide.render_slide()
    return (SlideCreator,)


@app.cell
def _():
    lehrstuhl = "Information Systems & Business Analytics"
    vorlesung = "Analytical Information Systems"
    presenter = "Christoph M. Flath"
    return lehrstuhl, presenter, vorlesung


@app.cell
def _(SlideCreator, lehrstuhl, presenter, vorlesung):
    sc = SlideCreator(lehrstuhl, vorlesung, presenter)
    return (sc,)


@app.cell
def _(sc):
    titleSlide = sc.create_slide("Data Management", layout_type="title-slide", newSection="Introduction")
    return (titleSlide,)


@app.cell
def _(mo, sc):
    hierarchy = sc.create_slide("Curated data is the foundation for analytics", layout_type="1-column")
    hierarchy.content1 = mo.image("public/AIS_02_DataManagement/AIS_02_Data_Management_2024_0.png", width=800, style={"margin-right": "auto", "margin-left": "auto"})
    return (hierarchy,)


@app.cell
def _(mo, sc):
    engingeeringvsmanagement = sc.create_slide("Data Engineering and Data Management", layout_type="side-by-side")
    engingeeringvsmanagement.content1 = mo.image("public/AIS_02_DataManagement/AIS_02_Data_Management_2024_2.png",
                                                              width=500,
                                                             caption="Topics in Data Engineering",
                                                             style={"margin-right": "auto", "margin-left": "auto"})
    engingeeringvsmanagement.content2 = mo.image("public/AIS_02_DataManagement/AIS_02_Data_Management_2024_1.png",
                                                              width=500,
                                                             caption="Topics in Data Management",
                                                              style={"margin-right": "auto", "margin-left": "auto"})
    return (engingeeringvsmanagement,)


@app.cell
def _(mo, sc):
    dataAndInformation = sc.create_slide("Data and Information", layout_type="side-by-side")
    dataAndInformation.content1 = mo.md(
            r"""
    * DATA:
        * Facts concerning people, objects, vents or other entities.
        * Data may be stored in files or in databases.
    * INFORMATION:
        * Data presented in a form suitable for interpretation.
        * Data is converted into information by programs and queries.
            * Neither files nor databases stores information.
    * KNOWLEDGE:
        * Insights into appropriate actions based on interpreted data.
        """
    )
    dataAndInformation.content2 = mo.md(
            r"""
    * DATABASE:
        * A shared collection of interrelated data designed to meet the varied information needs of an organization\.
        * Databases store data.
    * DATABASE MANAGEMENT SYSTEM:
        * A collection of programs to create and maintain a database.
        * Typical operations include:
            * Define
            * Construct
            * Manipulate
        """
    )
    return (dataAndInformation,)


@app.cell
def _(mo, sc):
    filesystem = '''
    block-beta
      columns 4
      M1["Metadata"] P1["Program 1"] space space
      space space space space
      M2["Metadata"] P2["Program 2"] space Data
      space space space space
      M3["Metadata"] P3["Program 3"] space space
      P1 --->  Data
      P2 --->  Data
      P3 --->  Data
      classDef program fill:#FFF
      classDef meta fill:#BBB
      class P1 program
      class P2 program
      class P3 program
      class M1 meta
      class M2 meta
      class M3 meta
      '''

    database = '''
    block-beta
      columns 4
      P1["Program 1"] space space space
      space space space space
      P2["Program 2"] space Data Metadata
      space space space space
      P3["Program 3"] space space space
      P1 --->  Data
      P2 --->  Data
      P3 --->  Data
      classDef meta fill:#BBB
      classDef program fill:#FFF
      class P1 program
      class P2 program
      class P3 program
      class Metadata meta
    '''

    dbVsFiles = sc.create_slide("Database vs File Systems", layout_type="side-by-side", newSection="Data Management and Databases")
    dbVsFiles.content1 = mo.vstack([mo.md(r"""**File system**"""), mo.mermaid(filesystem), mo.md(r"""Meta data is managed locally.""")])
    dbVsFiles.content2 = mo.vstack([mo.md(r"""**Database**"""),mo.mermaid(database), mo.md(r"""Meta data is managed centrally.""")])
    return (dbVsFiles,)


@app.cell
def _(mo, sc):
    dbReasons = sc.create_slide("Typical problems without using databases", layout_type="side-by-side")

    dbReasons.content1 = mo.md(
        r"""
    * Redundancy and inconsistency: Multiple storage locations, versioning problems
    * Inconsistent data formats
    * Multi-user operation: Lost Updates, Unrepeatable Reads
    * Data loss
    * Integrity Violation: Dependencies between entries
    * Security issues: Access protection
    * Development costs: No abstraction layer
        """
    )

    dbReasons.content2 = mo.md(
        r"""
    Database systems mitigate these issues by offering:

    * Data independence
    * Declarative query languages
    * Multi-user synchronization
    * Error handling
    * Data integrity
    * Efficiency and scalability

        """
    )
    return (dbReasons,)


@app.cell
def _(mo, sc):
    text = mo.md(
        r"""
    * Difficulties in designing the DB’s effectively brought design methodologies based on data models
    * Database development process
        * Conceptual Design: Produces the initial model of the real world in a conceptual model
        * Logical Design: Consists of transforming the conceptual schema into the data model supported by the DBMS
        * Implementation: Realizing the database in a specified DBMS

        """
    )

    designProces = """
    graph LR
        REQ[Business Information \n Requirements]
        A["Conceptual Data Modeling \n (Entity-Relationship Model)"]
        B["Logical Database Design \n (Relational Model)"]
        C["Implementation \n (SQL)"]
        OP[Operational \n Database]
        REQ -.-> A
        A --> B
        B --> C
        C -.-> OP
        style A fill:#d0e2f2,stroke:#000,stroke-width:1px
        style B fill:#d0e2f2,stroke:#000,stroke-width:1px
        style C fill:#d0e2f2,stroke:#000,stroke-width:1px
    """



    dbDesign = sc.create_slide("Database Design Phases", layout_type="1-column")
    dbDesign.content1 = mo.vstack(
        [
            text,
            mo.mermaid(designProces).style(
                {"margin-right": "auto", "margin-left": "auto", "width" : "100%"}
            ),
        ]
    )
    return (dbDesign,)


@app.cell
def _(mo, sc):
    conceptualDesign = sc.create_slide("Conceptual Design", layout_type="side-by-side", newSection="Conceptual Model")

    designProcessConceptual = """
    graph LR
        A["Conceptual Data Modeling \n (Entity-Relationship Model)"]
        B["Logical Database Design \n (Relational Model)"]
        C["Implementation \n (SQL)"]
        A --> B
        B --> C
        style A fill:lightgreen,stroke:#000,stroke-width:1px
        style B fill:#d0e2f2,stroke:#000,stroke-width:1px
        style C fill:#d0e2f2,stroke:#000,stroke-width:1px
    """
    conceptualDesign.content1 = mo.md(
            r"""
    * The process of constructing a model of the information used in an enterprise
        * Is a conceptual representation of the data structures
        * Is independent of all physical considerations
        * Should be simple enough to communicate with the end user
        * Should be detailed enough to create the physical structure
        """
    )

    conceptualDesign.content2 = mo.mermaid(designProcessConceptual)
    return (conceptualDesign,)


@app.cell
def _(mo, sc):
    conceptualDesign2 = sc.create_slide("Entity Relationship Diagram", layout_type="side-by-side")

    conceptualDesign2.content1 = mo.md(
            r"""
    * The Entity-Relationship model (ER) is the standard conceptual model for database design
        * No attention to efficiency or physical database design
        * Describes data as entities, attributes, and relationships
        * It is assumed that the Entity-Relationship diagram will be turned into one of the other available models during the logical design
        """
    )
    conceptualDesign2.content2 = mo.image("https://images.squarespace-cdn.com/content/v1/50c9c50fe4b0a97682fac903/1363727323947-GIDJVZ7P5RAFNI3DY70H/ERD1.jpg", width=600, caption="Example ER", style={"margin-right": "auto", "margin-left": "auto"})
    return (conceptualDesign2,)


@app.cell
def _(mo, sc):
    entitiesAttributes = sc.create_slide("Entities and Attributes", layout_type="2-column")
    entitiesAttributes.content1 = mo.md(
            r"""
    ___Entity___ 

    - “a thing that exists and is distinguishable” (J. Ullman)
    - A thing of significance about which the business needs to store information
    (e.g., employee, department)
    - Entity instance: an individual occurrence of a given entity
        (e.g., an employee named John Smith)


    ___Attribute___

    * Properties which describe the entity : id, name, address, age…
    * Attributes associate with each instance of an entity a value from a domain of values for that attribute
        * Set of integers, real numbers, character strings
        * Attributes can be optional or mandatory
        * Identifying attributes (e.g., SSN, ID) are underlined (key attributes)

        """
    )

    entitiesAttributes.content2 = mo.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/ERDiagramsInDBMS_5.png", width=500, caption="Student entity with four attributes", style={"margin-right": "auto", "margin-left": "auto"})
    return (entitiesAttributes,)


@app.cell
def _(mo, sc):
    relationships = sc.create_slide("Relationships", layout_type="side-by-side")

    textRelation =  mo.md(
    r"""
    - The diamond shape showcases a relationship in the ER diagram.
    - It chracterizes the relationship between two entities. (Employees are assigned to departments, employees are supervised by managers)
    - Cardinality specifies the number of instances of one entity that can or must be associated with each instance of another entity.
    """
    )


    relationships.content1 = textRelation
    relationships.content2 = mo.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/ERDiagramsInDBMS_10.png", width=500, caption="Example relationship", style={"margin-right": "auto", "margin-left": "auto"})
    return (relationships,)


@app.cell
def _(mo, sc):
    cardinality = sc.create_slide("Understanding Cardinality in DBMS (1/2)", layout_type="side-by-side")


    cardinality.content1 = mo.md("""

    - One-to-One Relationship
        - When a single element of an entity is associated with a single element of another entity, it is called a one-to-one relationship.
        - For example, a student has only one identification card and an identification card is given to one person.

    - One-to-Many Relationship

        - When a single element of an entity is associated with more than one element of another entity, it is called a one-to-many relationship
        - For example, a customer can place many orders, but an order cannot be placed by many customers.

    """
    )
    cardinality.content2 = mo.vstack([mo.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/ERDiagramsInDBMS_11.png", width=500, style={"margin-left": 5, "margin-right": "auto"}), mo.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/ERDiagramsInDBMS_12.png", width=500, style={ "margin-left": 5,"margin-right": "auto"})])
    return (cardinality,)


@app.cell
def _(mo, sc):
    cardinality2 = sc.create_slide("Understanding Cardinality in DBMS (2/2)", layout_type="side-by-side")
    cardinality2.content1 = mo.md("""

    - Many-to-One Relationship

        - When more than one element of an entity is related to a single element of another entity, then it is called a many-to-one relationship.
        - For example, students have to opt for a single course, but a course can have many students.

    - Many-to-Many Relationship

        - When more than one element of an entity is associated with more than one element of another entity, this is called a many-to-many relationship.
        - For example, you can assign an employee to many projects and a project can have many employees.


    """
    )
    cardinality2.content2 = mo.vstack([mo.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/ERDiagramsInDBMS_13.png", width=500, style={ "margin-left": 5,"margin-right": "auto"}), mo.image("https://www.simplilearn.com/ice9/free_resources_article_thumb/ERDiagramsInDBMS_14.png", width=500, style={ "margin-left": 5,"margin-right": "auto"})])
    return (cardinality2,)


@app.cell
def _(mo, sc):
    min_max_cardinality = sc.create_slide("Minimum and Maximum Cardinality", layout_type="side-by-side")

    min_max_cardinality.content1 = mo.md("""
    - To express cardinalities in a way that distinguishes between optional and necessary relationships we leverage the Min-Max-Notation
    - It allows to individually determine how often an entity has to enter a relationship at least and how often it can enter a relationship at most
    by using two (min, max)-pairs
    """
    )
    min_max_cardinality.content2 = mo.image("https://images.edrawsoft.com/articles/er-diagram-symbols/mix-max-notation.png", width=500, style={ "margin-left": 5,"margin-right": "auto"})
    return (min_max_cardinality,)


@app.cell
def _(mo, sc):
    example_er = sc.create_slide("Example ER Diagram", layout_type="1-column")
    example_er.content1 = mo.image("https://www.smartdraw.com/entity-relationship-diagram/img/erd-color.png", width=500, style={"margin-right": "auto", "margin-left": "auto"}
    )
    return (example_er,)


@app.cell
def _(mo, sc):
    logicalDesign = sc.create_slide("Logical Design", layout_type="side-by-side", newSection="Logical Model")

    designProcessLogical = """
    graph LR
        A["Conceptual Data Modeling \n (Entity-Relationship Model)"]
        B["Logical Database Design \n (Relational Model)"]
        C["Implementation \n (SQL)"]
        A --> B
        B --> C
        style A fill:#d0e2f2,stroke:#000,stroke-width:1px
        style B fill:lightgreen,stroke:#000,stroke-width:1px
        style C fill:#d0e2f2,stroke:#000,stroke-width:1px
    """

    logicalDesign.content1 = mo.md(
            r"""
    - Translate the conceptual representation into the logical data model supported by the DBMS 
    - The most popular model for database implementation nowadays is the relational model
        - Represents data in the form of relational tables
        - Relational database: Collection of relations or two-dimensional tables 
        - Ensures accuracy and consistency of the data by applying integrity constraint rules
        """
    )

    logicalDesign.content2 = mo.mermaid(designProcessLogical)
    return (logicalDesign,)


@app.cell
def _(mo, sc):
    RelationalTable = sc.create_slide("Relational Tables", layout_type="side-by-side")


    RelationalTable.content1 = mo.md(
            r"""
    - Every table has a unique name
    - Composed by named columns and unnamed rows
    - The rows represent occurrences of the entity
        - Every row is unique (ensured via a primary key)
        - Order of rows is irrelevant
    - Columns within a table have unique names
        - Order of columns is irrelevant
    - Every field value is atomic (contains a single value)
        """
    )

    RelationalTable.content2 = mo.md(
            r"""
    Special Columns

    - Primary Key
        - A column or a set of columns that uniquely identify each row in a table
        - Role is to enforce integrity - every table must have a non-null, unique primary key

    - Foreign Key
        - Column(s) in a table that serves as a PK of another table
        - Enforces referential integrity by completing an association between two tables

        """
    )
    return (RelationalTable,)


@app.cell
def _(mo, sc):
    Integrity = sc.create_slide("Data Integrity", layout_type="side-by-side")

    Integrity.content1 = mo.md(
            r"""

    We consider different integrity constraints

    - Entity Integrity: No part of a PK can be NULL
    - Referential Integrity: FK must match an existing PK value or else be NULL
    - Domain (Column) Integrity: A column must contain only values consistent with the defined data format of the column
    - User-defined Integrity: The data stored in the database must comply with the business rules

        """
    )

    Integrity.content2 = mo.image("public/AIS_02_DataManagement/integrity.png", width=500, style={"margin-right": "auto", "margin-left": "auto"})
    return (Integrity,)


@app.cell
def _(mo, sc):
    ER2Rel = sc.create_slide("From ER to Relational Model", layout_type="side-by-side")


    ER2Rel.content2 = mo.md(
            r"""
    - Binary 1:1 relationships
        - Introduce a foreign key in the table on the optional side

    - Binary 1:N relationship
        - Introduce a foreign key in the table on the ‘many’ side 

    - M:N relationships
        - Create a new table
        - Introduce as a composite Primary Key of the new table, the set of PKs of the original two tables



        """
    )

    ER2Rel.content1 = mo.image("public/AIS_02_DataManagement/ertorelation.png", width=500, style={"margin-right": "auto", "margin-left": "auto"})
    return (ER2Rel,)


@app.cell
def _(mo, sc):
    Normalization = sc.create_slide("Database Normalization", layout_type="side-by-side")
    Normalization.content1 = mo.md(r"""
    - A series of steps followed to obtain a database design that allows for consistent storage and avoiding duplication of data
        - In the process relationships with anomalies are decomposed into smaller, well-structured relations
    - The normalization process passes through fulfilling different Normal Forms
        - A table is said to be in a certain normal form if it satisfies certain constraints
        - Originally, Codd defined three Normal Forms, later on several more were added

    For most practical purposes databases are considered normalized if they adhere to 3rd Normal Form
        """
    )
    Normalization.content2 = mo.image("public/AIS_02_DataManagement/normalization.png", style={"margin-right": "auto", "margin-left": "auto"})
    return (Normalization,)


@app.cell
def _(mo, sc):
    firstsecondNF = sc.create_slide("First and Second Normal Form", layout_type="side-by-side")



    firstsecondNF.content1 = mo.md(
            r"""
    -  1st Normal Form
        - All table attributes’ values must be atomic, multi-values are not allowed
        - By definition a relational table is in 1st Normal Form

    - 2nd Normal Form
        - Every non-key attribute is fully functionally dependent on the PK (no partial dependencies)
        - Approach: For each attribute in the PK that is involved in a partial dependency, create a new table
    all attributes that are partially dependent on that attribute should be moved to the new table




        """
    )

    firstsecondNF.content2 = mo.image("public/AIS_02_DataManagement/normalization2.png", width=350, style={"margin-right": "auto", "margin-left": "auto"})
    return (firstsecondNF,)


@app.cell
def _(mo, sc):
    thirdNF = sc.create_slide("Third Normal Form", layout_type="side-by-side")
    thirdNF.content1 = mo.md(
            r"""
    - No transitive dependencies for non-key attributes
    - Transitive dependence: When a non-key attribute depends on another non-key attribute.
    - Approach:
        - For each non-key attribute A that depends upon another non-key attribute B create a new table
        - Create PK of the new table as attribute B
        - Create a FK in the original table referencing the PK of the new table




        """
    )

    thirdNF.content2 = mo.image("public/AIS_02_DataManagement/thirdNF.png", width=350, style={"margin-right": "auto", "margin-left": "auto"})
    return (thirdNF,)


@app.cell
def _(mo, sc):
    denorm = sc.create_slide("Denormalization", layout_type="side-by-side")

    denorm.content1 = mo.md(
            r"""
    - Queries against a fully normalized database often perform poorly
        - Current RDBMSs implement the relational model poorly.
    - Two approaches are used to overcome this issue
        - Keep the logical design normalized but allow the DBMS to store additional redundant information on disk to optimize query response (indexes, materialized views, etc.).
            - In this case it is the DBMS software's responsibility to ensure that any redundant copies are kept consistent.



        """
    )

    denorm.content2 = mo.vstack([mo.md(
            r"""
    - Use denormalization to improve performance, at the cost of reduced consistency 
        - Denormalization is the process of attempting to optimize the performance of a database by adding redundant data 
        - There should be a new set of constraints added that specify how the redundant copies of information must be kept synchronized 
        """), mo.image("public/AIS_02_DataManagement/denormalization.png", width=350, style={"margin-right": "auto", "margin-left": "auto"})])
    return (denorm,)


@app.cell
def _(mo, sc):
    sql = sc.create_slide("Structured Query Language (SQL)", layout_type="side-by-side", newSection="Implementation with SQL")



    sql.content1 = mo.md(
            r"""
    - Most commonly implemented relational query language
    - originally developed by IBM
    - official ANSI standard
    - Provides different command types:
        - SQL as Data Definition Language (DDL): Create, modify, delete tables
        - SQL as Data Query Language (DQL): Execute queries on tables
        - SQL as Data Manipulation Language (DML): Insert, modify, delete data in tables
        - SQL as Data Control Language (DCL): User and transaction management
        - SQL as Transaction Control Language (TCL): Transaction management
        """
    )

    sql.content2 = mo.image("public/AIS_02_DataManagement/sqlCommands.png", width=500, style={"margin-right": "auto", "margin-left": "auto"})
    return (sql,)


@app.cell
def _(mo, sc):
    ddl = sc.create_slide("Data Definition Language (DDL)", layout_type="side-by-side")

    ddl.content1 = mo.md(
            r"""
    - Database schema is a collection of logical structures of data 
    - The implementation of the database schema is realized through the DDL part of SQL
    - Although there is a standard for SQL, there might be some features when writing the SQL scripts that are vendor specific




        """
    )

    ddl.content2 = mo.md(
            r"""
    - CREATE table - describes the layout of the table by providing
        - table name
        - column names 
        - datatype for each column
        - integrity constraints – PK, FK, column constraints, default values, not null

    - DROP, ALTER, RENAME are used to interact with previously created tables






        """
    )
    return (ddl,)


@app.cell
def _(mo, sc):
    dml = sc.create_slide("Data Manipulation Language (DML)", layout_type="side-by-side")

    dml.content1 = mo.md(
            r"""
    - DML is used to insert, update, delete, and query data within an existing database schema.
    - Data manipulation is executed through the DML subset of SQL, allowing users to interact directly with the data stored in database tables.
    - Standard SQL defines basic DML commands, but there are variations and additional features that can be vendor-specific.
    - DML statements may trigger integrity constraint checks (like foreign keys or primary keys), and transactions are frequently used to maintain database consistency.




        """
    )

    dml.content2 = mo.md(
            r"""
    - INSERT – adds new records into tables

    - UPDATE – modifies existing records based on specified criteria

    - DELETE – removes records from tables based on specified conditions

    - SELECT – queries and retrieves data from one or more tables using conditions, filters, sorting, and grouping






        """
    )
    return (dml,)


@app.cell
def _(mo, sc):
    dql_intro = sc.create_slide("Data Query Language (DQL)", layout_type="one-column")

    dql_intro.content1 = mo.md(
        r"""
    - **DQL** (Data Query Language) is the part of SQL responsible for retrieving data from databases.
    - It is essential for exploring, analyzing, and understanding stored information.
    - DQL statements do **not** modify the data—they are read-only operations.
    - Foundation for reporting and analytics
    - Enables filtering, sorting, and drilling into data
    - Forms the basis for dashboards, BI tools, and machine learning pipelines

    What's Coming:

    - Basic SELECT queries (columns, filtering, ordering)
    - Multi-table queries with JOIN

    """
    )
    return (dql_intro,)


@app.cell
def _(mo, sc):
    dql_key_elements = sc.create_slide("Key Elements of SELECT Statements", layout_type="side-by-side")

    dql_key_elements.content1 = mo.md(
        r"""
    The basic structure of a **SELECT** query includes several essential clauses:

    ```sql
    SELECT column_list
    FROM table_name
    WHERE conditions
    ORDER BY column(s)
    LIMIT number_of_rows;
    ```

    Each clause performs a specific role in the query process.
    """
    )

    dql_key_elements.content2 = mo.md(
        r"""
    - **SELECT**: Specifies the columns to retrieve.
    - **FROM**: Indicates the source table or tables.
    - **WHERE**: Filters the rows based on specific conditions.
    - **ORDER BY**: Sorts the results according to specified criteria.
    - **LIMIT**: Restricts the number of rows returned by the query.

    These elements help define precisely what data is retrieved from the database.
    """
    )
    return (dql_key_elements,)


@app.cell
def _(mo, sc):
    fbi_crime_data = sc.create_slide("FBI Crime Data Set Overview", layout_type="one-column")

    fbi_crime_data.content1 = mo.md(
        r"""
    - The data originates from the FBI's Uniform Crime Reporting (UCR) Program, which has been collecting and publishing crime statistics since 1930.

    - The dataset encompasses nationwide crime statistics, detailing various offenses

    - The dataset spans from 1960 to 2018, offering a comprehensive view of crime trends over nearly six decades.

        - It is instrumental in analyzing long-term crime trends, understanding the impact of policy changes, and supporting criminological research and public policy development.

    - Data Structure:

        - Population: Total U.S. population for each year.
        - Year: The specific year of the data.
        - Crime Rates: Number of reported incidents per 100,000 inhabitants for each crime category (column names: homicide, rape, robbery, aggravated_assault, burglary,larceny, motor_vehicle_theft).
        """
    )
    return (fbi_crime_data,)


@app.cell
def _(StringIO, pd):
    crime = pd.read_csv(StringIO("""population,year,homicide,rape,robbery,aggravated_assault,burglary,larceny,motor_vehicle_theft
    179323175,1960,5,10,60,86,509,1035,183
    181712050,1961,5,9,58,86,519,1045,184
    184100925,1962,5,9,60,89,535,1125,197
    186489800,1963,5,9,62,92,576,1219,217
    188878675,1964,5,11,68,106,635,1316,247
    191267550,1965,5,12,72,111,663,1329,257
    193656425,1966,6,13,81,120,721,1443,287
    196045300,1967,6,14,103,130,827,1576,334
    198434175,1968,7,16,132,144,932,1747,393
    200823050,1969,7,19,148,155,984,1931,436
    203211926,1970,8,19,172,165,1085,2079,457
    205545314,1971,9,21,188,179,1164,2146,460
    207878702,1972,9,23,181,189,1141,1994,426
    210212090,1973,9,25,183,201,1223,2072,443
    212545478,1974,10,26,209,216,1438,2490,462
    214878866,1975,10,26,221,231,1532,2805,474
    217212254,1976,9,27,199,233,1448,2921,450
    219545642,1977,9,29,191,240,1420,2730,452
    221879030,1978,9,31,196,262,1435,2747,461
    220099000,1979,10,35,218,286,1512,2999,506
    225349264,1980,10,37,251,298,1684,3167,502
    229465714,1981,10,36,258,289,1647,3135,474
    231664458,1982,9,34,239,289,1488,3083,459
    233791994,1983,8,34,217,279,1339,2871,431
    235824902,1984,8,36,206,291,1266,2795,438
    237923795,1985,8,37,209,304,1292,2911,464
    240132887,1986,9,38,226,347,1350,3022,510
    242288918,1987,8,38,214,353,1336,3095,532
    244498982,1988,8,38,222,372,1316,3152,586
    246819230,1989,9,38,234,386,1284,3190,634
    249464396,1990,9,41,256,423,1232,3185,656
    252153092,1991,10,42,273,433,1252,3229,659
    255029699,1992,9,43,264,442,1168,3104,632
    257782608,1993,10,41,256,441,1100,3034,606
    260327021,1994,9,39,238,428,1042,3027,591
    262803276,1995,8,37,221,418,987,3043,560
    265228572,1996,7,36,202,391,945,2980,526
    267783607,1997,7,36,186,382,919,2892,506
    270248003,1998,6,34,165,361,863,2729,460
    272690813,1999,6,33,150,334,770,2551,422
    281421906,2000,6,32,145,324,729,2477,412
    285317559,2001,6,32,148,319,742,2486,431
    287973924,2002,6,33,146,310,747,2451,433
    290788976,2003,6,32,142,295,741,2416,434
    293656842,2004,5,32,137,289,730,2362,422
    296507061,2005,6,32,141,291,727,2288,417
    299398484,2006,6,32,150,292,733,2213,400
    301621157,2007,6,31,148,287,726,2185,365
    304059724,2008,5,30,146,277,733,2166,315
    307006550,2009,5,29,133,265,718,2064,259
    309330219,2010,5,28,119,253,701,2006,239
    311587816,2011,5,27,114,241,701,1974,230
    313873685,2012,5,27,113,243,672,1965,230
    316497531,2013,5,36,109,230,610,1902,221
    318907401,2014,4,37,101,229,537,1822,215
    320896618,2015,5,39,102,238,495,1784,222
    323405935,2016,5,41,103,248,469,1745,237
    325147121,2017,5,42,99,249,430,1696,238
    327167434,2018,5,43,86,247,376,1595,229"""))
    return


@app.cell
def _(mo):
    def getQueryEditor(query, nrows=7):
        return(mo.ui.text_area(label="SQL Query", value=query, full_width=True, rows=nrows))
    return (getQueryEditor,)


@app.cell
def _(getQueryEditor):
    queryEditor = getQueryEditor("SELECT * FROM 'crime';")
    return (queryEditor,)


@app.cell
def _(mo, queryEditor, sc):
    sql_query = sc.create_slide("Our first SQL query", layout_type="side-by-side")

    try:
        queryResult = mo.sql(queryEditor.value, output=False)
        table_display = mo.ui.table(
            queryResult,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display = mo.md(f"**Error:** {str(e)}")
    sql_query.content1 = mo.vstack([
        mo.md(r"""

        - SELECT first specifies the columns to be returned, * means all columns

        - FROM specifies the table to be queried, here crime is the table of the FBI crime data

        - Therefore, we are selecting all columns and rows from the crime table

        - For datasets with many columns and rows, it is often useful to restrict the output returned

        ---
        """),
        mo.hstack([queryEditor,mo.md("")],widths=[9,1])
    ])

    sql_query.content2 = table_display
    return (sql_query,)


@app.cell
def _(getQueryEditor):
    queryEditor2 = getQueryEditor("""SELECT year,
    ROUND(homicide * population / 100000) AS homicideCount,
    5 as Constant5
    FROM 'crime';""")
    return (queryEditor2,)


@app.cell
def _(mo, queryEditor2, sc):
    sql_query2 = sc.create_slide("Renaming and creating new columns", layout_type="side-by-side")

    try:
        queryResult2 = mo.sql(queryEditor2.value, output=False)
        table_display2 = mo.ui.table(
            queryResult2,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display2 = mo.md(f"**Error:** {str(e)}")

    sql_query2.content1 = mo.vstack([
        mo.md(r"""

        - AS is used to rename columns or create new columns

        - New columns can be calculated from existing columns or using constants

        ---
        """),
        mo.hstack([queryEditor2,mo.md("")],widths=[9,1])
    ])

    sql_query2.content2 = table_display2
    return (sql_query2,)


@app.cell
def _(getQueryEditor):
    queryEditor3 = getQueryEditor("""SELECT year,
    homicide
    FROM 'crime'
    ORDER BY homicide DESC
    LIMIT 10;""")
    return (queryEditor3,)


@app.cell
def _(mo, queryEditor3, sc):
    sql_query3 = sc.create_slide("Limiting and ordering the output", layout_type="side-by-side")


    try:
        queryResult3 = mo.sql(queryEditor3.value, output=False)
        table_display3 = mo.ui.table(
            queryResult3,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display3 = mo.md(f"**Error:** {str(e)}")


    sql_query3.content1 = mo.vstack([
        mo.md(r"""

        - A simple way for limiting the number of rows is the LIMIT n command which restricts the number of rows returned to the first n rows

        - ORDER BY is used to sort the output based on the specified column, the suffix DESC or ASC specifies descending order

        ---
        """),
        mo.hstack([queryEditor3,mo.md("")],widths=[9,1])
    ])

    sql_query3.content2 = table_display3
    return (sql_query3,)


@app.cell
def _(getQueryEditor):
    queryEditorAgg = getQueryEditor("""SELECT
        AVG(homicide) AS avg_homicide,
        MIN(robbery) AS min_robbery,
        MAX(burglary) AS max_burglary
    FROM crime;""", 7)
    return (queryEditorAgg,)


@app.cell
def _(mo, queryEditorAgg, sc):
    agg_slide = sc.create_slide("Aggregate Functions: AVG, MIN, MAX", layout_type="side-by-side")

    try:
        queryResultAgg = mo.sql(queryEditorAgg.value, output=False)
        table_display_agg = mo.ui.table(
            queryResultAgg,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display_agg = mo.md(f"**Error:** {str(e)}")

    agg_slide.content1 = mo.vstack(
        [
            mo.md(
                r"""
        - Aggregate functions allow you to perform calculations on a set of values and return a single result.

        - `AVG()` calculates the average value.
        - `MIN()` finds the minimum value.
        - `MAX()` finds the maximum value.

        - In this example, we are calculating the average homicide rate, the minimum robbery rate, and the maximum burglary rate across all years in the `crime` table.

        ---
        """
            ),
            mo.hstack([queryEditorAgg,mo.md("")],widths=[9,1])
        ]
    )

    agg_slide.content2 = table_display_agg
    return (agg_slide,)


@app.cell
def _(getQueryEditor):
    query_editor_where = getQueryEditor("""SELECT year, homicide, robbery
    FROM crime
    WHERE year > 2000 AND homicide < 10;""")
    return (query_editor_where,)


@app.cell
def _(mo, query_editor_where, sc):
    where_clause = sc.create_slide("Filtering Rows with WHERE", layout_type="side-by-side")

    try:
        query_result_where = mo.sql(query_editor_where.value, output=False)
        table_display_where = mo.ui.table(
            query_result_where,
            show_column_summaries=False,
            selection=None,
            show_download=False,
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display_where = mo.md(f"**Error:** {str(e)}")

    where_clause.content1 = mo.vstack(
        [
            mo.md(
                r"""
        - The `WHERE` clause filters rows based on specified conditions.

        - You can use comparison operators (=, >, <, >=, <=, !=) and logical operators (AND, OR, NOT) to create complex conditions.

        ---
        """
            ),
            mo.hstack([query_editor_where,mo.md("")],widths=[9,1])
        ]
    )

    where_clause.content2 = table_display_where
    return (where_clause,)


@app.cell
def _(getQueryEditor):
    queryEditorCase = getQueryEditor("""SELECT
        year,
        CASE
            WHEN homicide > 10 THEN 'High'
            WHEN homicide > 5 THEN 'Medium'
            ELSE 'Low'
        END AS homicide_level
    FROM crime;""", 7)
    return (queryEditorCase,)


@app.cell
def _(mo, queryEditorCase, sc):
    case_slide = sc.create_slide("Conditional Logic with CASE Statements", layout_type="side-by-side")

    try:
        queryResultCase = mo.sql(queryEditorCase.value, output=False)
        table_display_case = mo.ui.table(
            queryResultCase,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display_case = mo.md(f"**Error:** {str(e)}")

    case_slide.content1 = mo.vstack(
        [
            mo.md(
                r"""
        - The `CASE` statement allows you to define conditional logic within your SQL queries.

        - It evaluates conditions and returns different values based on whether those conditions are met.

        - In this example, we are categorizing homicide rates as 'High', 'Medium', or 'Low' based on their values.

        ---
        """
            ),
            mo.hstack([queryEditorCase,mo.md("")],widths=[9,1])
        ]
    )

    case_slide.content2 = table_display_case
    return (case_slide,)


@app.cell
def _(mo, sc):
    subquery_intro_slide = sc.create_slide("Introduction to Subqueries", layout_type="one-column")

    subquery_intro_slide.content1 = mo.md(
        r"""
    - A **subquery** is a query nested inside another SQL query.

    - It is used to retrieve data that will be used in the main query as a condition to further restrict the data to be selected.

    - Subqueries can be used in the `SELECT`, `FROM`, and `WHERE` clauses.

    - **Benefits of Using Subqueries:**

        - **Modularity:** Break down complex queries into smaller, more manageable parts.
        - **Readability:** Improve the clarity of your SQL code.
        - **Flexibility:** Perform complex filtering and data manipulation.

    - **Key Considerations:**

        - Subqueries are executed once before the main query.
        - Performance can be a concern with poorly written subqueries.
        - Ensure the subquery returns a compatible data type for the outer query.
    """
    )
    return (subquery_intro_slide,)


@app.cell
def _(getQueryEditor):
    queryEditorSubqueryMin = getQueryEditor("""SELECT year, homicide
    FROM crime
    WHERE homicide = (SELECT MIN(homicide) FROM crime);""", 7)
    return (queryEditorSubqueryMin,)


@app.cell
def _(mo, queryEditorSubqueryMin, sc):
    subquery_min_slide = sc.create_slide("Subquery Example", layout_type="side-by-side")

    try:
        queryResultSubqueryMin = mo.sql(queryEditorSubqueryMin.value, output=False)
        table_display_subquery_min = mo.ui.table(
            queryResultSubqueryMin,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display_subquery_min = mo.md(f"**Error:** {str(e)}")

    subquery_min_slide.content1 = mo.vstack(
        [
            mo.md(
                r"""
        - This query uses a subquery to find the year with the lowest homicide rate.

        - The subquery `(SELECT MIN(homicide) FROM crime)` finds the minimum homicide rate in the entire dataset.

        - The outer query then selects the `year` and `homicide` columns from the `crime` table where the `homicide` rate matches the minimum value found by the subquery.

        ---
        """
            ),
            mo.hstack([queryEditorSubqueryMin,mo.md("")],widths=[9,1])
        ]
    )

    subquery_min_slide.content2 = table_display_subquery_min
    return (subquery_min_slide,)


@app.cell
def _(StringIO, pd):
    income = pd.read_csv(StringIO("""year,median income,margin of error
    1984,"51,742",235
    1985,"52,709",286
    1986,"54,608",283
    1987,"55,260",269
    1988,"55,716",284
    1989,"56,678",312
    1990,"55,952",286
    1991,"54,318",260
    1992,"53,897",255
    1993,"53,610",251
    1994,"54,233",247
    1995,"55,931",323
    1996,"56,744",286
    1997,"57,911",268
    1998,"60,040",355
    1999,"61,526",287
    2000,"61,399",193
    2001,"60,038",183
    2002,"59,360",195
    2003,"59,286",257
    2004,"59,080",261
    2005,"59,712",200
    2006,"60,178",258
    2007,"60,985",170
    2008,"58,811",160
    2009,"58,400",250
    2010,"56,873",375
    2011,"56,006",281
    2012,"55,900",229
    2013,"57,856",706
    2014,"56,969",416
    2015,"59,901",340
    2016,"61,779",456
    2017,"62,868",343
    2018,"63,179",420"""), decimal=".", sep=",", header=0, names=["year","medIncome","error"])
    income["medIncome"] = income["medIncome"].str.replace(",", "").astype(float)
    return


@app.cell
def _(getQueryEditor):
    queryEditorJoin = getQueryEditor("""SELECT
        crime.year,
        crime.homicide,
        income.medIncome
    FROM
        crime
    JOIN
        income ON crime.year = income.year;
    """, 10)
    return (queryEditorJoin,)


@app.cell
def _(mo, queryEditorJoin, sc):
    join_slide = sc.create_slide("Joining Tables", layout_type="side-by-side")

    try:
        queryResultJoin = mo.sql(queryEditorJoin.value, output=False)
        table_display_join = mo.ui.table(
            queryResultJoin,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display_join = mo.md(f"**Error:** {str(e)}")

    join_slide.content1 = mo.vstack(
        [
            mo.md(
                r"""
        - The `JOIN` clause combines rows from two or more tables based on a related column.

        - In this case, we are joining the `crime` table with the `income` table on the `year` column.

        - Different types of JOINs exist (INNER, LEFT, RIGHT, FULL), but here we use an INNER JOIN, which returns rows only when there is a match in both tables.

        ---
        """
            ),
            mo.hstack([queryEditorJoin,mo.md("")],widths=[9,1])
        ]
    )

    join_slide.content2 = table_display_join
    return (join_slide,)


@app.cell
def _(getQueryEditor):
    queryEditorJoin2 = getQueryEditor("""SELECT
        crime.year,
        crime.homicide /
        income.medIncome AS hi_ratio
    FROM
        crime
    JOIN
        income ON crime.year = income.year;
    """, 10)
    return (queryEditorJoin2,)


@app.cell
def _(mo, queryEditorJoin2, sc):
    join_slide2 = sc.create_slide("Joining Tables Extension", layout_type="side-by-side")

    try:
        queryResultJoin2 = mo.sql(queryEditorJoin2.value, output=False)
        table_display_join2 = mo.ui.table(
            queryResultJoin2,
            show_column_summaries=False,
            selection=None,
            show_download=False
        ).style({"margin-right": "auto", "margin-left": "auto"})
    except Exception as e:
        table_display_join2 = mo.md(f"**Error:** {str(e)}")

    join_slide2.content1 = mo.vstack(
        [
            mo.md(
                r"""
        - Before we just combined the two data sets by reporting columns simultaneously.

        - This extended example joins the `crime` and `income` tables on the `year` column, as before. However, it then calculates a new column, `hi_ratio`, by dividing the `homicide` rate from the `crime` table by the median income (`medIncome`) from the `income` table. 

        - The resulting table displays the year and the calculated `hi_ratio` which provides a normalized measure, potentially indicating the relationship between homicide rates and economic factors.  

        ---
        """
            ),
            mo.hstack([queryEditorJoin2,mo.md("")],widths=[9,1])
        ]
    )

    join_slide2.content2 = table_display_join2
    return (join_slide2,)


@app.cell
def _(titleSlide):
    titleSlide.render_slide()
    return


@app.cell
def _(sc):
    sc.create_agenda(currentSection="Introduction")
    return


@app.cell
def _(hierarchy):
    hierarchy.render_slide()
    return


@app.cell
def _(engingeeringvsmanagement):
    engingeeringvsmanagement.render_slide()
    return


@app.cell
def _(dataAndInformation):
    dataAndInformation.render_slide()
    return


@app.cell
def _(sc):
    sc.create_agenda(currentSection="Data Management and Databases")
    return


@app.cell
def _(dbVsFiles):
    dbVsFiles.render_slide()
    return


@app.cell
def _(dbReasons):
    dbReasons.render_slide()
    return


@app.cell
def _(dbDesign):
    dbDesign.render_slide()
    return


@app.cell
def _(sc):
    sc.create_agenda(currentSection="Conceptual Model")
    return


@app.cell
def _(conceptualDesign):
    conceptualDesign.render_slide()
    return


@app.cell
def _(conceptualDesign2):
    conceptualDesign2.render_slide()
    return


@app.cell
def _(entitiesAttributes):
    entitiesAttributes.render_slide()
    return


@app.cell
def _(relationships):
    relationships.render_slide()
    return


@app.cell
def _(cardinality):
    cardinality.render_slide()
    return


@app.cell
def _(cardinality2):
    cardinality2.render_slide()
    return


@app.cell
def _(min_max_cardinality):
    min_max_cardinality.render_slide()
    return


@app.cell
def _(example_er):
    example_er.render_slide()
    return


@app.cell
def _(sc):
    sc.create_agenda(currentSection="Logical Model")
    return


@app.cell
def _(logicalDesign):
    logicalDesign.render_slide()
    return


@app.cell
def _(RelationalTable):
    RelationalTable.render_slide()
    return


@app.cell
def _(Integrity):
    Integrity.render_slide()
    return


@app.cell
def _(ER2Rel):
    ER2Rel.render_slide()
    return


@app.cell
def _(Normalization):
    Normalization.render_slide()
    return


@app.cell
def _(firstsecondNF):
    firstsecondNF.render_slide()
    return


@app.cell
def _(thirdNF):
    thirdNF.render_slide()
    return


@app.cell
def _(denorm):
    denorm.render_slide()
    return


@app.cell
def _(sc):
    sc.create_agenda(currentSection="Implementation")
    return


@app.cell
def _(sql):
    sql.render_slide()
    return


@app.cell
def _(ddl):
    ddl.render_slide()
    return


@app.cell
def _(dml):
    dml.render_slide()
    return


@app.cell
def _(dql_intro):
    dql_intro.render_slide()
    return


@app.cell
def _(dql_key_elements):
    dql_key_elements.render_slide()
    return


@app.cell
def _(fbi_crime_data):
    fbi_crime_data.render_slide()
    return


@app.cell
def _(sql_query):
    sql_query.render_slide()
    return


@app.cell
def _(sql_query2):
    sql_query2.render_slide()
    return


@app.cell
def _(sql_query3):
    sql_query3.render_slide()
    return


@app.cell
def _(agg_slide):
    agg_slide.render_slide()
    return


@app.cell
def _(where_clause):
    where_clause.render_slide()
    return


@app.cell
def _(case_slide):
    case_slide.render_slide()
    return


@app.cell
def _(subquery_intro_slide):
    subquery_intro_slide.render_slide()
    return


@app.cell
def _(subquery_min_slide):
    subquery_min_slide.render_slide()
    return


@app.cell
def _(join_slide):
    join_slide.render_slide()
    return


@app.cell
def _(join_slide2):
    join_slide2.render_slide()
    return


if __name__ == "__main__":
    app.run()
