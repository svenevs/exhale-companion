__all__ = ['generate_all_files', 'TextRoot', 'TextNode']








#
# woaaaah way too much duplication
#
#
# this is what you should do: stack based DFS with a queue,
#    start at root.get_compound()
#    add them all in there to ze queue as you go
#    track namespaces and files and classes independently
#
#    then you will probably need to bring the doxygen xml parsing
#        back into play to get the remaining things you were missing???
#        *** find a way to grab the include path from the doxygen xml
#            because breathe meses it up. you should be able to do it
#            while gathering the refid's you are missing
#
#
#
# ** File: BaseClass.h
#   - [class]:     arbitrary::BaseClass
#   - [class]:     arbitrary::BaseClass
#   - [variable]:  some_data
#   - [function]:  ~BaseClass
#   - [function]:  getData
#   - [function]:  BaseClass
#   - [struct]:    arbitrary::nested::int2
#   - [struct]:    arbitrary::nested::int2
#   - [variable]:  x
#   - [variable]:  y
#   - [function]:  int2
#   - [function]:  int2
#   - [struct]:    arbitrary::nested::dual_nested::int3
#   - [struct]:    arbitrary::nested::dual_nested::int3
#   - [variable]:  x
#   - [variable]:  y
#   - [variable]:  z
#   - [function]:  int3
#   - [function]:  int3
#   - [namespace]: arbitrary
#     - member: enum, CAMERA_STATES
#     - member: enumvalue, CAM_NONE
#     - member: enumvalue, CAM_ROTATE
#     - member: enumvalue, CAM_TRANSLATE
#     - member: enumvalue, CAM_SCALE
#   - [namespace]: arbitrary::nested
#   - [namespace]: arbitrary::nested::dual_nested
#   - [file]:      common.h
#   - [file]:      DerivedClass.h
#   - [define]:    AN_ARBITRARY_DEFINE
# ** File: common.h
#   - [struct]:    super_params
#   - [variable]:  x
#   - [variable]:  y
#   - [variable]:  z
#   - [function]:  super_params
#   - [function]:  super_params
#   - [union]:     super_params::U
#   - [variable]:  first_view
#   - [variable]:  second_view
#   - [namespace]: external
#     - member: variable, MAX_DEPTH
#   - [file]:      BaseClass.h
#   - [typedef]:   super_bool
#   - [file]:      DerivedClass.h
#   - [typedef]:   super_bool
#   - [variable]:  common_float_variable
#   - [function]:  someCommonFunction
# ** File: DerivedClass.h
#   - [class]:     arbitrary::BaseClass
#   - [class]:     arbitrary::BaseClass
#   - [class]:     arbitrary::DerivedClass
#   - [class]:     arbitrary::DerivedClass
#   - [function]:  ~DerivedClass
#   - [function]:  virtualMethod
#   - [function]:  insertAt
#   - [function]:  itemAt
#   - [namespace]: arbitrary
#     - member: enum, CAMERA_STATES
#     - member: enumvalue, CAM_NONE
#     - member: enumvalue, CAM_ROTATE
#     - member: enumvalue, CAM_TRANSLATE
#     - member: enumvalue, CAM_SCALE
#   - [file]:      BaseClass.h
#   - [file]:      common.h
# ****************************************************************
# ** Namespace: __global__namespace__
#   - [struct]:    super_params
# ** Namespace: arbitrary
#   - [class]:     arbitrary::BaseClass
#   - [class]:     arbitrary::DerivedClass
#   - [enum]:      CAMERA_STATES
# ** Namespace: arbitrary::nested
#   - [struct]:    arbitrary::nested::int2
# ** Namespace: arbitrary::nested::dual_nested
#   - [struct]:    arbitrary::nested::dual_nested::int3
# ** Namespace: external
#   - [variable]:  MAX_DEPTH
# (nspace) : arbitrary
#     (nspace) : arbitrary::nested
#         (nspace) : arbitrary::nested::dual_nested
#             (struct) : arbitrary::nested::dual_nested::int3
#         (struct) : arbitrary::nested::int2
#     (class) : arbitrary::BaseClass
#     (class) : arbitrary::DerivedClass
# (nspace) : external
# (nspace) : Unscoped Global Namespace
#     (struct) : super_params































#
# Note: known crash on struct params
#
from breathe.parser.index import parse as breathe_parse
import sys
import re

EXHALE_API_TOCTREE_MAX_DEPTH = 5
'''Larger than 5 will likely produce errors with a LaTeX build, but the user can
   override this value by supplying a different value to `generate_all_files`.'''

EXHALE_API_DOXY_OUTPUT_DIR = ""

def generate_all_files(root_generated_file, root_generated_title,
                       root_after_title_description, doxygen_xml_index_path,
                       toctree_max_depth=5):
    '''
    document me please
    '''
    global EXHALE_API_TOCTREE_MAX_DEPTH
    EXHALE_API_TOCTREE_MAX_DEPTH = toctree_max_depth
    breathe_root = None

    try:
        global EXHALE_API_DOXY_OUTPUT_DIR
        EXHALE_API_DOXY_OUTPUT_DIR = doxygen_xml_index_path.split('index.xml')[0]
    except:
        sys.stderr.write("Unable to parse the doxygen root directory based off the doxygen_xml_index_path provided.")

    try:
        # breathe_root = breathe_parse('./doxyoutput/xml/index.xml')
        breathe_root = breathe_parse(doxygen_xml_index_path)
    except:
        sys.stderr.write("Could not use 'breathe' to parse the root 'doxygen' index.xml.\n")

    if breathe_root is not None:
        text_root = TextRoot(breathe_root, root_generated_file, root_generated_title, root_after_title_description)
        # for n in text_root.namespaces:
        #     n.toConsole(0)


# discovered types
#
#    doxygenclass     <-+-> "class"
#    doxygendefine    <-+-> "define"
#    doxygenenum      <-+-> "enum"
#    doxygenenumvalue <-+-> "enumvalue"
#    doxygenfile      <-+-> "file"
#    autodoxygenfile  <-+-> IGNORE
#    doxygenfunction  <-+-> "function"
#    doxygengroup     <-+-> "group" UNSUPPORTED
#    doxygenindex     <-+-> IGNORE
#    autodoxygenindex <-+-> IGNORE
#    doxygennamespace <-+-> "namespace"
#    doxygenstruct    <-+-> "struct"
#    doxygentypedef   <-+-> "typedef"
#    doxygenunion     <-+-> BROKEN IN BREATHE
#    doxygenvariable  <-+-> "variable"
#
# Observations:
#    - The doxygen union stuff works on doxygen html output, but
#      breathe produces something weird.
#    - typedef, variable, function etc are children of file sometimes
#      not sure what to do with organizing those automatically
#    - strangely, the "namespace" doesn't have BaseClass and DerivedClass
#      associated with it from breathe.  quick hack would be to instead
#      gather a list of everything, and if the name is 'namespace::thing'
#      then create your own hierarchy
#    - groups seem to be broken in breathe, no children appear with them
#      and fixing that one would be a lot of work and probably still not work
#
#    For my purposes, I think all I want to grab is the class, struct, and function?
#

# enums show up in the namespace member list, classes, structs, and functions do not
class TextNode(object):
    """docstring for TextNode"""
    def __init__(self, parent, breathe_compound, breathe_name, breathe_kind):
        super(TextNode, self).__init__()
        self.parent = parent
        self.compound = breathe_compound
        self.name = breathe_name
        self.kind = breathe_kind
        self.children = []
        self.link_name = None
        self.file_name = None
        if breathe_compound is not None:
            self.refid = self.compound.get_refid()
        else:
            self.refid = "#"

    def add_child(self, child):
        child_already_added = False
        for c in self.children:
            print("+++ [self={}] -- [child={}] +++".format(self.name, child.name))
            if c.name == child.name:
                child_already_added = True
                print("*********************************************")
                break

        if not child_already_added:
            self.children.append(child)
            child.parent = self

    def strip(self):
        pop_indices = []
        # for idx in range(len(self.children)):
        #     child_kind = self.children[idx].kind
        #     if child_kind == "enum" or child_kind == "enumvalue" or child_kind == "variable" or \
        #        child_kind == "namespace":
        #         pop_indices.append(idx)

        # for idx in reversed(sorted(pop_indices)):
        #     self.children.pop(idx)

    @classmethod
    def qualifyKind(cls, kind):
        """
        Qualifies the breathe ``kind`` and returns an qualifier string describing this
        to be used for the text output.

        :type:  class
        :param: cls
            The `TextNode` class.

        :type:  str
        :param: kind
            The return value of a Breathe ``compound`` object's ``get_kind()`` method.

        :rtype: str
        :return:
            The qualifying string that will be used to build the restructured text output
            and sidebar in the class hierarchies.  If the empty string is returned then
            it should be ignored / not added as a child.
        """
        qualifier = ""
        if kind == "class":
            qualifier = "(class)"
        elif kind == "struct":
            qualifier = "(struct)"
        elif kind == "function":
            qualifier = "(fun)"
        elif kind == "enum":
            qualifier = "(enum)"
        elif kind == "enumvalue":
            pass
        elif kind == "namespace":
            qualifier = "(nspace)"
        elif kind == "define":
            qualifier = "(def)"
        elif kind == "typedef":
            qualifier = "(tdef)"
        elif kind == "variable":
            qualifier = "(var)"
        elif kind == "file":
            qualifier = "(file)"
        else:
            qualifier = "(_<<<{}>>>_)".format(kind)

        return qualifier

    @classmethod
    def kindAsBreatheDirective(cls, kind):
        directive = ""
        if kind == "class":
            directive = "doxygenclass"
        elif kind == "struct":
            directive = "doxygenstruct"
        elif kind == "function":
            directive = "doxygenfunction"
        elif kind == "enum":
            directive = "doxygenenum"
        # elif kind == "enumvalue":
        #     pass
        elif kind == "namespace":
            directive = "doxygennamespace"
        elif kind == "define":
            directive = "doxygendefine"
        elif kind == "typedef":
            directive = "doxygentypedef"
        elif kind == "variable":
            directive = "doxygenvariable"
        elif kind == "file":
            directive = "doxygenfile"

        return directive

    @classmethod
    def directivesForKind(cls, kind):
        if kind == "class":
            directive = "   :members:\n   :protected-members:\n   :undoc-members:\n"
        elif kind == "struct":
            directive = "   :members:\n   :protected-members:\n   :undoc-members:\n"
        elif kind == "function":
            directive = ""
        elif kind == "enum":
            directive = ""
        elif kind == "enumvalue":
            directive = ""
        elif kind == "namespace":
            directive = "   :members:\n"
        elif kind == "define":
            directive = ""
        elif kind == "typedef":
            directive = ""
        elif kind == "variable":
            directive = ""
        elif kind == "file":
            directive = ""
        else:
            directive = ""

        return directive

    def toConsole(self, indent_level):
        indent = " " * (indent_level * 4)
        qualifier = TextNode.qualifyKind(self.kind)
        if qualifier != "":
            qualifier = "{} : ".format(qualifier)
        else:
            print("**********************{}*******************".format(self.name))

        print("{}{}{}".format(indent, qualifier, self.name))
        for c in self.children:
            c.toConsole(indent_level + 1)

    def enumerate(self, indent_level, enum_link_file_list, generated_label_to_file_map):
        indent = " " * (indent_level * 4)

        qualifier = TextNode.qualifyKind(self.kind)
        if qualifier != "":
            qualifier = "{} : ".format(qualifier)
        else:
            print("**********************{}*******************".format(self.name))

        self.link_name = self.name.replace(":", "_")
        self.file_name = "generated_api_{}.rst".format(self.link_name)

        # every namespace gets its own file that children will append to
        if self.kind == "namespace":
            if self.name == "":
                self.name = "Unscoped Global Namespace"
                self.link_name = self.name.replace(' ', '_')
                self.file_name = "generated_api_{}.rst".format(self.link_name)
                self.file_name = "generated_api_unscoped_global_namespace.rst"
            try:
                with open(self.file_name, "w") as gen_file:
                    # generate a link label for every generated file
                    link_declaration = ".. _{}:\n\n".format(self.link_name)
                    # every generated file must have a header for sphinx to be happy
                    header = "Namespace ``{}``\n========================================================================================\n\n".format(self.name.split("::")[-1])
                    # inject the appropriate doxygen directive and name of this node
                    # directive = ".. {}:: {}\n".format(TextNode.kindAsBreatheDirective(self.kind), self.name)
                    # include any specific directives for this doxygen directive
                    # specifications = "{}\n\n".format(TextNode.directivesForKind(self.kind))
                    gen_file.write("{}{}".format(link_declaration, header))
            except:
                raise RuntimeError("Critical error while generating the file for [{}]".format(self.name))

            # nested namespaces need a little extra care, only one level for the toctree
            # to avoid confusing layouts
            if self.parent.name != "ROOT" and self.parent.kind == "namespace":
                with open(self.parent.file_name, "a") as parent_file:
                    parent_file.write(
                        ".. toctree::\n"
                        "   :maxdepth: 1\n\n"
                        "   {}\n\n".format(self.file_name)
                    )
        elif self.parent.name != "ROOT" and self.parent.kind == "namespace":
            try:
                # generate the file for this node
                with open(self.file_name, "w") as gen_file:
                    # generate a link label for every generated file
                    link_declaration = ".. _{}:\n\n".format(self.link_name)
                    # every generated file must have a header for sphinx to be happy
                    # header = "{}\n========================================================================================\n\n".format(self.name.split("::")[-1])
                    header = "{}\n----------------------------------------------------------------------------------------\n\n".format(self.name.split("::")[-1])
                    # inject the appropriate doxygen directive and name of this node
                    directive = ".. {}:: {}\n".format(TextNode.kindAsBreatheDirective(self.kind), self.name)
                    # include any specific directives for this doxygen directive
                    specifications = "{}\n\n".format(TextNode.directivesForKind(self.kind))
                    gen_file.write("{}{}{}{}".format(link_declaration, header, directive, specifications))

                # add this node to the parent namespace, toctree maxdepth of 1 since there
                # will only be one item listed in this newly generated file
                with open(self.parent.file_name, "a") as parent_file:
                    parent_file.write(
                        ".. toctree::\n"
                        "   :maxdepth: 1\n\n"
                        "   {}\n\n".format(self.file_name)
                    )
            except:
                raise RuntimeError("Critical error while generating the file for [{}]".format(self.name))


        # self_enum = "{}- ``{}`` :ref:`{}`".format(indent, qualifier, self.link_name)
        # member_enum = ""
        # try:
        #     with open(self.file_name, "w") as gen_file:
        #         # generate a link label for every generated file
        #         link_declaration = ".. _{}:\n\n".format(self.link_name)
        #         # every generated file must have a header for sphinx to be happy
        #         header = "{}\n========================================================================================\n\n".format(self.name.split("::")[-1])
        #         # inject the appropriate doxygen directive and name of this node
        #         directive = ".. {}:: {}\n".format(TextNode.kindAsBreatheDirective(self.kind), self.name)
        #         # include any specific directives for this doxygen directive
        #         specifications = "{}\n\n".format(TextNode.directivesForKind(self.kind))
        #         gen_file.write("{}{}{}{}".format(link_declaration, header, directive, specifications))
        # except:
        #     raise RuntimeError("Critical error while generating the file for [{}]".format(self.name))

        # if self.compound is not None and "member" in self.compound.__dict__:
        #     member_indent = "    {}".format(indent)
        #     for member in self.compound.get_member():
        #         member_kind = member.get_kind()
        #         member_name = member.get_name()

        #         member_qualifier = TextNode.qualifyKind(member_kind)
        #         if member_qualifier != "":
        #             member_qualifier = "{} : ".format(member_qualifier)
        #             member_enum += "\n{}- {}{} :ref:`{}`".format(member_indent, member_qualifier, member_name, member.get_refid())

        # # append this to the list of enumerations
        # enumeration_string = "{}{}".format(self_enum, member_enum)
        # enum_link_file_list.append((enumeration_string, self.link_name, self.file_name, self.refid))

        # # add this generated pair to the map parameter
        # generated_label_to_file_map[self.link_name] = enumeration_string

        for c in self.children:
            c.enumerate(indent_level+1, enum_link_file_list, generated_label_to_file_map)

    def namespaced_add_child(self, child):
        if self.kind != "namespace":
            return False

        parts = child.name.split("::")
        num_parts = len(parts)
        if(num_parts <= 1):
            return False

        resolved_name = parts.pop(-1) # grabs the last one
        prepended_namespace = "::".join(p for p in parts)

        if self.name == prepended_namespace:
            self.children.append(child)
            child.parent = self
            return True
        else:
            for c in self.children:
                if c.namespaced_add_child(child):
                    return True

        return False

class Node:
    # if you change these deliberately you are at fault
    WHITE = 0
    GREY  = 1
    BLACK = 2

    def __init__(self, breathe_compound):
        self.compound = breathe_compound
        self.kind     = breathe_compound.get_kind()
        self.name     = breathe_compound.get_name()
        self.refid    = breathe_compound.get_refid()
        self.color    = Node.WHITE
        self.children = []

    def colorWhite(self):
        self.color = Node.WHITE

    def colorGrey(self):
        self.color = Node.GREY

    def colorBlack(self):
        self.color = Node.BLACK

    def toConsole(self, level):
        indent = "  " * level
        print("{}- [{}]: {}".format(indent, self.kind, self.name))
        for c in self.children:
            c.toConsole(level+1)



class TextRoot(object):
    """docstring for TextRoot"""
    def __init__(self, breathe_root, root_file_name, root_file_title, root_file_description):
        super(TextRoot, self).__init__()
        self.name = "ROOT" # used in the TextNode class
        self.breathe_root = breathe_root
        self.class_like = [] # list of TextNodes
        self.namespaces = []
        self.all_compounds = []
        self.top_level = []
        self.dirs = []
        self.files = []
        self.root_file_name = root_file_name
        self.root_file_title = root_file_title
        self.root_file_description = root_file_description


        ### merge to be just one dictionary, find way that works for key traversal
        ### for py2 and py3
        self.namespace_names = []
        self.namespace_children = {}
        self.namespace_names.append("__global__namespace__")
        self.namespace_children["__global__namespace__"] = []


        # graph root set in parse....or just now
        self.all_compounds = [self.breathe_root.get_compound()]
        self.all_nodes = []
        self.namespaces = []
        self.unions = []
        self.files = []
        self.class_like = []
        self.enums = []
        self.dirs = []


        #--------------------+----------------+
        # autodoxygenfile  <-+-> IGNORE       |
        # doxygenindex     <-+-> IGNORE       |
        # autodoxygenindex <-+-> IGNORE       |
        #--------------------+----------------+
        # doxygenclass     <-+-> "class"      |
        # doxygenstruct    <-+-> "struct"     |
        self.class_like      = [] #           |
        # doxygendefine    <-+-> "define"     |
        self.defines         = [] #           |
        # doxygenenum      <-+-> "enum"       |
        self.enums           = [] #           |
        # ---> largely ignored by framework,  |
        #      but stored if desired          |
        # doxygenenumvalue <-+-> "enumvalue"  |
        self.enum_values     = [] #           |
        # doxygenfunction  <-+-> "function"   |
        self.functions       = [] #           |
        # doxygenfile      <-+-> "file"       |
        self.files           = [] #           |
        # not used, but could be supported in |
        # the future?                         |
        # doxygengroup     <-+-> "group"      |
        self.groups          = [] #           |
        # doxygennamespace <-+-> "namespace"  |
        self.namespaces      = [] #           |
        # doxygentypedef   <-+-> "typedef"    |
        self.typedefs        = [] #           |
        # doxygenunion     <-+-> "union"      |
        self.unions          = [] #           |
        # doxygenvariable  <-+-> "variable"   |
        self.variables       = [] #           |
        #-------------------------------------+

        self.__parse()
        # self.__post_process()
        # self.__strip()
        # self.__enumerate()

    def trackNodeIfUnseen(self, node):
        '''
        if node is not in self.all_nodes yet, add it to both self.all_nodes as well as
        the corresponding self.<node.kind> list
        '''
        if node not in self.all_nodes:
            self.all_nodes.append(node)
            if node.kind == "class" or node.kind == "struct":
                self.class_like.append(node)
            elif node.kind == "namespace":
                self.namespaces.append(node)
            elif node.kind == "enum":
                self.enums.append(node)
            elif node.kind == "enumvalue":
                self.enum_values.append(node)
            elif node.kind == "define":
                self.defines.append(node)
            elif node.kind == "file":
                self.files.append(node)
            elif node.kind == "dir":
                self.dirs.append(node)
            elif node.kind == "function":
                self.functions.append(node)
            elif node.kind == "variable":
                self.variables.append(node)
            elif node.kind == "group":
                self.groups.append(node)
            elif node.kind == "typedef":
                self.typedefs.append(node)
            elif node.kind == "union":
                self.unions.append(node)
        else:
            print("&&&&&&&&&&&&&&&&&&&&&&: {}, {}".format(node.kind, node.name))

    def discoverNeigbors(self, nodes_remaining, node):
        # discover neighbors of current node; some seem to not have get_member()
        if "member" in node.compound.__dict__:
            for member in node.compound.get_member():
                # keep track of every breathe compound we have seen
                if member not in self.all_compounds:
                    self.all_compounds.append(member)
                    # if we haven't seen this compound yet, make a node
                    child_node = Node(member)
                    # if the current node is a class, struct, union, or enum it's
                    # ignore variables, functions, etc
                    if node.kind != "class" and node.kind != "struct" and node.kind != "union":
                        nodes_remaining.append(child_node)
                    # the enum is also presented, no need for separate enumvals
                    # ... determining the enumvalue parent would be painful and i don't want to do it
                    if child_node.kind != "enumvalue":
                        node.children.append(child_node)

    def discoverAllNodes(self):
        '''
        stack based traversal of breathe graph, termination will have populated

        self.all_compounds, self.all_nodes, self.<breathe_kind>
        '''
        # When you call the breathe_root.get_compound() method, it returns a list of the
        # top level source nodes.  These start out on the stack, and we add their
        # children if they have not already been visited before.
        nodes_remaining = [Node(compound) for compound in self.breathe_root.get_compound()]
        while len(nodes_remaining) > 0:
            curr_node = nodes_remaining.pop()
            print("NODE: {}{}{}".format(curr_node.name, "__>><<__", curr_node.kind))
            self.trackNodeIfUnseen(curr_node)
            self.discoverNeigbors(nodes_remaining, curr_node)

    def reparentUnions(self):
        '''
        namespaces and classes should have the unions defined in them to be in the child
        list of itself rather than floating around.

        removes reparented unions from self.unions
        '''
        pop_indices = []
        for idx in range(len(self.unions)):
            u = self.unions[idx]
            parts = u.name.split("::")
            num_parts = len(parts)
            if num_parts > 1:
                # it can either be a child of a namespace or a class_like
                if num_parts > 2:
                    namespace_name  = "::".join(p for p in parts[:-2])
                    potential_class = parts[-2]

                    # see if it belongs to a class like object first. if so, remove this
                    # union from the list of unions
                    reparented = False
                    for cl in self.class_like:
                        if cl.name == potential_class:
                            cl.children.append(u)
                            pop_indices.insert(0, idx)
                            reparented = True
                            break

                    if reparented:
                        continue

                    # otherwise, see if it belongs to a namespace
                    alt_namespace_name = "{}::{}".format(namespace_name, potential_class)
                    for n in self.namespaces:
                        if namespace_name == n.name or alt_namespace_name == n.name:
                            n.children.append(u)
                            # # do not pop this for global presentation of unions
                            # reparented = True
                            break
                else:
                    name_or_class_name = "::".join(p for p in parts[:-1])

                    # see if it belongs to a class like object first. if so, remove this
                    # union from the list of unions
                    reparented = False
                    for cl in self.class_like:
                        if cl.name == name_or_class_name:
                            cl.children.append(u)
                            pop_indices.insert(0, idx)
                            reparented = True
                            break

                    if reparented:
                        continue

                    # next see if it belongs to a namespace
                    for n in self.namespaces:
                        if n.name == name_or_class_name:
                            n.children.append(u)
                            break

        if len(pop_indices) > 0:
            for idx in pop_indices:
                self.unions.pop(idx)

    def reparentAll(self):
        '''
        reparents unions to class like objects or namespaces (and removes from self.unions)

        adds classes to namespaces, but keeps the class like objects in their list
        '''
        self.reparentUnions()

    def __parse(self):
        for x in range(99):
            print("{}".format(x*"+"))

        self.discoverAllNodes()
        self.reparentAll()


        print("###########################################################")
        print("## {}".format("Classes and Structs"))
        print("###########################################################")
        for n in self.class_like:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Defines"))
        print("###########################################################")
        for n in self.defines:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Enums"))
        print("###########################################################")
        for n in self.enums:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Enum Values"))
        print("###########################################################")
        for n in self.enum_values:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Functions"))
        print("###########################################################")
        for n in self.functions:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Files"))
        print("###########################################################")
        for n in self.files:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Directories"))
        print("###########################################################")
        for d in self.dirs:
            d.toConsole(0)
        print("###########################################################")
        print("## {}".format("Groups"))
        print("###########################################################")
        for n in self.groups:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Namespaces"))
        print("###########################################################")
        for n in self.namespaces:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Typedefs"))
        print("###########################################################")
        for n in self.typedefs:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Unions"))
        print("###########################################################")
        for n in self.unions:
            n.toConsole(0)
        print("###########################################################")
        print("## {}".format("Variables"))
        print("###########################################################")
        for n in self.variables:
            n.toConsole(0)


        for x in range(99, 0, -1):
            print("{}".format(x*"+"))






        # for compound in self.breathe_root.get_compound():
        #     compound_name = compound.get_name()
        #     compound_kind = compound.get_kind()
        #     compound_refid = compound.get_refid()

        #     self.all_compounds.append((compound, compound_kind, compound_name, compound_refid))

        #     if compound_kind == "namespace":
        #         # first time we are seeing this namespace
        #         if compound_name not in self.namespace_names:
        #             self.namespace_names.append(compound_name)
        #             self.namespace_children[compound_name] = []
        #     else:
        #         parts = compound_name.split("::")
        #         num_parts = len(parts)
        #         if num_parts > 1:
        #             if compound_kind != "union":
        #                 namespace_name  = "::".join(p for p in parts[:-1])
        #                 # first time we are seeing this namespace (e.g. before it appeared in breathe hierarchy)
        #                 if namespace_name not in self.namespace_names:
        #                     self.namespace_names.append(namespace_name)
        #                     self.namespace_children[namespace_name] = []

        #                 if compound_kind != "class" and compound_kind != "struct" and compound_kind == "variable":
        #                     self.namespace_children[namespace_name].append((compound, compound_kind, compound_name, compound_refid))
        #                     self.all_compounds.append((compound, compound_kind, compound_name, compound_refid))
        #                 elif compound_kind != "variable":
        #                     self.namespace_children[namespace_name].append((compound, compound_kind, compound_name, compound_refid))
        #                     self.all_compounds.append((compound, compound_kind, compound_name, compound_refid))
        #         elif compound_kind != "group" and compound_kind != "file" and compound_kind != "dir":
        #             self.namespace_children["__global__namespace__"].append((compound, compound_kind, compound_name, compound_refid))

        #     # if compound_kind != "class" and compound_kind != "struct" and "member" in compound.__dict__:
        #     if "member" in compound.__dict__:
        #         for n_compound in compound.get_member():
        #             n_compound_name = n_compound.get_name()
        #             n_compound_kind = n_compound.get_kind()
        #             n_compound_refid = n_compound.get_refid()

        #             # compound variables of structs and classes need to be ignored
        #             if compound_kind != "class" and compound_kind != "struct" and compound_kind == "variable":
        #                 # add everything to the namespaces
        #                 if compound_kind == "namespace":
        #                     self.namespace_children[compound_name].append((n_compound, n_compound_kind, n_compound_name, n_compound_refid))
        #                 # add the variable to the list of all compounds
        #                 self.all_compounds.append((n_compound, n_compound_kind, n_compound_name, n_compound_refid))
        #             elif compound_kind != "variable":
        #                 # add everything to the namespaces
        #                 if compound_kind == "namespace":
        #                     namespaced = compound_name.split("::")
        #                     self.namespace_children[compound_name].append((n_compound, n_compound_kind, n_compound_name, n_compound_refid))
        #                 # add the variable to the list of all compounds
        #                 self.all_compounds.append((n_compound, n_compound_kind, n_compound_name, n_compound_refid))

        #     #
        #     # classify the current compound for building the index tree
        #     #
        #     # namespaces are treated specially
        #     if compound_kind == "namespace":
        #         namespace_node = TextNode(self, compound, compound_name, compound_kind)
        #         self.namespaces.append(namespace_node)

        #         # namespaces have some members such as `enum` correctly listed in the
        #         # breathe compound's member list
        #         for member in compound.get_member():
        #             member_name = member.get_name()
        #             member_kind = member.get_kind()
        #             namespace_node.namespaced_add_child(TextNode(self, member, member_name, member_kind))

        #     # files are treated specially
        #     elif compound_kind == "file":
        #         file_node = TextNode(self, compound, compound_name, compound_kind)
        #         self.files.append(file_node)

        #         # files have members such as 'define' or 'function'
        #         # for member in compound.get_member():
        #         #     member_name = member.get_name()
        #         #     member_kind = member.get_kind()
        #         #     file_node.add_child(TextNode(self, member, member_name, member_kind))

        #     # # directories are treated specially
        #     # elif compound_kind == "dir":
        #     #     pass
        #     #     # print("DIR: {}".format(compound_name))
        #     #     # for m in compound.get_member():
        #     #     #     print("  {}: {}".format(m.get_name(), m.get_kind()))

        #     # unions appear to be completely broken in breathe, groups do not have their members
        #     elif compound_kind == "union":# or compound_kind == "group":
        #         pass

        #     # At this point, we have already checked for
        #     #
        #     #   - namespace
        #     #   - file
        #     #   - dir
        #     #   - union and group (ignore)
        #     #
        #     # and are left with the following types that are either already owned by a
        #     # 'file' or a 'namespace':
        #     #
        #     #   - define
        #     #   - function
        #     #   - typedef
        #     #   - variable
        #     #
        #     # so the above will either appear in a 'get_member()' list from 'file' or
        #     # 'namespace'.  What remains is for us to process the class-like objects:
        #     #
        #     #   - class
        #     #   - struct
        #     #
        #     # and check the name of them, to subclass them to the appropriate namespace
        #     # if / where applicable.  Before that can be done, though, the nested
        #     # namespaces need to be arranged first.
        #     elif compound_kind == "class" or compound_kind == "struct":
        #         self.class_like.append(TextNode(self, compound, compound_name, compound_kind))
        #     else:
        #         print("*********************** 999999999999999999999")
        #         self.top_level.append(TextNode(self, compound, compound_name, compound_kind))

    def __post_process(self):
        # First, we need to account for nested namespaces
        namespace_pop_indices = []
        num_namespaces = len(self.namespaces)

        for curr_idx in range(num_namespaces):
            nspace = self.namespaces[curr_idx]
            parts  = nspace.name.split("::")

            if len(parts) > 1:
                for idy in range(num_namespaces):
                    if self.namespaces[idy].namespaced_add_child(nspace):
                        namespace_pop_indices.append(curr_idx)
                        break

        for remove_idx in reversed(sorted(namespace_pop_indices)):
            self.namespaces.pop(remove_idx)

        # add a final namespace text node to house any items not declared in a namespace
        self.namespaces.append(TextNode(self, None, "", "namespace"))

        # Now that nested namespaces are accounted for, add all the class-like objects
        # to their appropriate namespaces
        clike_pop_indices = []
        num_clike = len(self.class_like)
        for curr_idx in range(num_clike):
            clike = self.class_like[curr_idx]
            parts = clike.name.split("::")

            if len(parts) > 1:
                found_home = False
                for idx in range(len(self.namespaces)-1): # ignore last "global" namespace
                    nspace = self.namespaces[idx]
                    if nspace.namespaced_add_child(clike):
                        clike_pop_indices.append(curr_idx)
                        found_home = True
                        break

                # if we reach this part then something went wrong
                if not found_home:
                    raise RuntimeError("The class [{}] split on '::' could not find a namespace home.".format(clike.name))
            else:
                self.namespaces[-1].add_child(clike)
                clike_pop_indices.append(curr_idx)

        for remove_idx in reversed(sorted(clike_pop_indices)):
            self.class_like.pop(remove_idx)

    def __strip(self):
        for n in self.namespaces:
            n.strip()

    def __enumerate(self):
        # list of (enumeration_string, link_name, file_name, refid)
        namespace_enumerations = []
        # namespace_enumerations.append("Class Hierarchy")
        # namespace_enumerations.append("=============================================")
        namespace_link_to_file_map = {}
        for n in self.namespaces:
            n.enumerate(0, namespace_enumerations, namespace_link_to_file_map)


        file_enumerations = []
        # file_enumerations.append("\n\nFile Hierarchy")
        # file_enumerations.append("=============================================")
        file_link_to_file_map = {}
        for f in self.files:
            f.enumerate(0, file_enumerations, file_link_to_file_map)

        print("\n\n:::::::::::::::::::::::::::::::::::::::::::")
        print(":::::::::::::::::::::::::::::::::::::::::::")
        print(":::::::::::::::::::::::::::::::::::::::::::\n\n")

        print("Num total compounds: {}".format(len(self.all_compounds)))
        print("Total class_like:    {}".format(len(self.class_like)))
        print("Total namespaces:    {}".format(len(self.namespaces)))
        print("Total files:         {}".format(len(self.files)))
        print("Total top_level:     {}".format(len(self.top_level)))
        print("Total dirs:          {}".format(len(self.dirs)))

        try:
            with open(self.root_file_name, "w") as generated_index:
                generated_index.write("{}\n".format(self.root_file_title))
                generated_index.write("==============================================================\n\n")
                generated_index.write("{}\n\n".format(self.root_file_description))
                # for link_name, file_name in GENERATED_FILES:
                #     generated_index.write(
                #         ".. toctree::\n"
                #         "   :maxdepth: 1\n\n"
                #         "   {}\n\n".format(file_name)
                #     )

                for n in self.namespaces:
                    generated_index.write(
                        ".. toctree::\n"
                        "   :maxdepth: {}\n\n"
                        "   {}\n\n".format(EXHALE_API_TOCTREE_MAX_DEPTH, n.file_name)
                    )

                # keys: file object, values: list of refid's
                doxygen_xml_file_ownerships = {}
                regex = re.compile(r'.*refid="(\w+)".*')
                for f in self.files:
                    if EXHALE_API_DOXY_OUTPUT_DIR != "":
                        doxygen_xml_file_ownerships[f] = []
                        try:
                            doxy_xml_path = "{}{}.xml".format(EXHALE_API_DOXY_OUTPUT_DIR, f.refid)
                            with open(doxy_xml_path, "r") as doxy_file:
                                # all_lines = doxy_file.readlines()
                                for line in doxy_file:
                                    match = regex.match(line)
                                    if match is not None:
                                        doxygen_xml_file_ownerships[f].append(match.groups()[0])

                        except:
                            sys.stderr.write("Unable to process doxygen xml for file [{}].\n".format(f.name))

                print("++++++++++++++++++++++++++++++++++++++++++++++++")
                print("++++++++++++++++++++++++++++++++++++++++++++++++")
                print("++++++++++++++++++++++++++++++++++++++++++++++++")
                print(doxygen_xml_file_ownerships)
                # reduce this to build in opposite way......
                # build list first of only refids that exist during
                # construction
                print("++++++++++++++++++++++++++++++++++++++++++++++++")
                print("++++++++++++++++++++++++++++++++++++++++++++++++")
                print("++++++++++++++++++++++++++++++++++++++++++++++++")

                all_file_ownerships = {}

                # initialize all of the dictionaries
                for f in self.files:
                    all_file_ownerships[f] = []

                # parse all of the breath compounds found previously and attach them to
                # the file that defines them
                for compound, kind, name, refid in self.all_compounds:
                    for f in self.files:
                        if refid in doxygen_xml_file_ownerships[f]:
                            all_file_ownerships[f].append((compound, kind, name, refid))

                for f in self.files:
                    for compound in f.compound.get_member():
                        kind  = compound.get_kind()
                        name  = compound.get_name()
                        refid = compound.get_refid()
                        all_file_ownerships[f].append((compound, kind, name, refid))

                # now that we have all the compounds sorted by file, we need to take an
                # extra step with namespaces.  when a variable [[ TEST: OR UNION ]] is
                # in a namespace...wait....functions???
                for f in self.files:
                    print("** File: {}".format(f.name))
                    for compound, kind, name, refid in all_file_ownerships[f]:
                        if kind == "class":
                            print("  - [class]:     {}".format(name))
                        elif kind == "struct":
                            print("  - [struct]:    {}".format(name))
                        elif kind == "function":
                            print("  - [function]:  {}".format(name))
                        elif kind == "enum":
                            print("  - [enum]:      {}".format(name))
                        elif kind == "enumvalue":
                            pass
                        elif kind == "union":
                            print("  - [union]:     {}".format(name))
                        elif kind == "namespace":
                            print("  - [namespace]: {}".format(name))
                            for m in compound.get_member():
                                print("    - member: {}, {}".format(m.get_kind(), m.get_name()))
                        elif kind == "define":
                            print("  - [define]:    {}".format(name))
                        elif kind == "typedef":
                            print("  - [typedef]:   {}".format(name))
                        elif kind == "variable":
                            print("  - [variable]:  {}".format(name))
                        elif kind == "file":
                            print("  - [file]:      {}".format(name))
                        else:
                            print("  - ?????????????????? {}".format(name))

                print("****************************************************************")
                for n in self.namespace_names:
                    print("** Namespace: {}".format(n))
                    for compound, kind, name, refid in self.namespace_children[n]:
                        if kind == "class":
                            print("  - [class]:     {}".format(name))
                        elif kind == "struct":
                            print("  - [struct]:    {}".format(name))
                        elif kind == "function":
                            print("  - [function]:  {}".format(name))
                        elif kind == "enum":
                            print("  - [enum]:      {}".format(name))
                        elif kind == "enumvalue":
                            pass
                        elif kind == "union":
                            print("  - [union]:     {}".format(name))
                        elif kind == "namespace":
                            print("  - [namespace]: {}".format(name))
                            for m in compound.get_member():
                                print("    - member: {}, {}".format(m.get_kind(), m.get_name()))
                        elif kind == "define":
                            print("  - [define]:    {}".format(name))
                        elif kind == "typedef":
                            print("  - [typedef]:   {}".format(name))
                        elif kind == "variable":
                            print("  - [variable]:  {}".format(name))
                        elif kind == "file":
                            print("  - [file]:      {}".format(name))
                        else:
                            print("  - ?????????????????? {}".format(name))



                        # print("  - {}".format(c.get_name()))

                    # # generate the full file documentation
                    # try:
                    #     with open(f.file_name, "w") as full_file:
                    #         # generate a link label for every generated file
                    #         link_declaration = ".. _{}:\n\n".format(f.link_name)
                    #         # every generated file must have a header for sphinx to be happy
                    #         # header = "{}\n========================================================================================\n\n".format(self.name.split("::")[-1])
                    #         header = "{}\n----------------------------------------------------------------------------------------\n\n".format(f.name)
                    #         # inject the appropriate doxygen directive and name of this node
                    #         directive = ".. {}:: {}\n".format(TextNode.kindAsBreatheDirective(f.kind), f.name)
                    #         # include any specific directives for this doxygen directive
                    #         specifications = "{}\n\n".format(TextNode.directivesForKind(f.kind))
                    #         full_file.write("{}{}{}{}".format(link_declaration, header, directive, specifications))
                    # except Exception as e:
                    #     sys.stderr.write("Unable to generate the documentation for file [{}].\n".format(f.name))

                    # generated_index.write(
                    #     ".. toctree::\n"
                    #     "   :maxdepth: {}\n\n"
                    #     "   {}\n\n".format(EXHALE_API_TOCTREE_MAX_DEPTH, f.file_name)
                    # )
        except Exception as e:
            sys.stderr.write("(!) Exception caught during enumeration of library api: {}\n".format(e))
