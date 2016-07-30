__all__ = ['generate_all_files', 'TextRoot', 'TextNode']

#
# Note: known crash on struct params
#
from breathe.parser.index import parse as breathe_parse
import sys

def generate_all_files(root_generated_file, root_generated_title, doxygen_xml_index_path):
    '''
    document me please
    '''
    breathe_root = None
    try:
        # breathe_root = breathe_parse('./doxyoutput/xml/index.xml')
        breathe_root = breathe_parse(doxygen_xml_index_path)
    except:
        sys.stderr.write("Could not use 'breathe' to parse the root 'doxygen' index.xml.\n")

    if breathe_root is not None:
        text_root = TextRoot(breathe_root)
        for n in text_root.namespaces:
            n.toConsole(0)


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
        self.parent = parent # None if it is the root
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

            # nested namespaces need a little extra care
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

                # add this node to the parent namespace
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


class TextRoot(object):
    """docstring for TextRoot"""
    def __init__(self, breathe_root):
        super(TextRoot, self).__init__()
        self.name = "ROOT" # used in the TextNode class
        self.breathe_root = breathe_root
        self.class_like = [] # list of TextNodes
        self.namespaces = []
        self.all_compounds = []
        self.top_level = []
        self.dirs = []
        self.files = []
        self.__parse()
        self.__post_process()
        self.__strip()
        self.__enumerate()

    def __parse(self):
        for compound in self.breathe_root.get_compound():
            compound_name = compound.get_name()
            compound_kind = compound.get_kind()

            self.all_compounds.append((compound, compound_kind, compound_name))

            #
            # classify the current compound for building the index tree
            #
            # namespaces are treated specially
            if compound_kind == "namespace":
                namespace_node = TextNode(self, compound, compound_name, compound_kind)
                self.namespaces.append(namespace_node)

                # namespaces have some members such as `enum` correctly listed in the
                # breathe compound's member list
                for member in compound.get_member():
                    member_name = member.get_name()
                    member_kind = member.get_kind()
                    namespace_node.namespaced_add_child(TextNode(self, member, member_name, member_kind))

            # files are treated specially
            elif compound_kind == "file":
                file_node = TextNode(self, compound, compound_name, compound_kind)
                self.files.append(file_node)

                # files have members such as 'define' or 'function'
                # for member in compound.get_member():
                #     member_name = member.get_name()
                #     member_kind = member.get_kind()
                #     file_node.add_child(TextNode(self, member, member_name, member_kind))

            # directories are treated specially
            elif compound_kind == "dir":
                pass
                # print("DIR: {}".format(compound_name))
                # for m in compound.get_member():
                #     print("  {}: {}".format(m.get_name(), m.get_kind()))

            # unions appear to be completely broken in breathe, groups do not have their members
            elif compound_kind == "union" or compound_kind == "group":
                continue

            # At this point, we have already checked for
            #
            #   - namespace
            #   - file
            #   - dir
            #   - union and group (ignore)
            #
            # and are left with the following types that are either already owned by a
            # 'file' or a 'namespace':
            #
            #   - define
            #   - function
            #   - typedef
            #   - variable
            #
            # so the above will either appear in a 'get_member()' list from 'file' or
            # 'namespace'.  What remains is for us to process the class-like objects:
            #
            #   - class
            #   - struct
            #
            # and check the name of them, to subclass them to the appropriate namespace
            # if / where applicable.  Before that can be done, though, the nested
            # namespaces need to be arranged first.
            elif compound_kind == "class" or compound_kind == "struct":
                self.class_like.append(TextNode(self, compound, compound_name, compound_kind))
            else:
                self.top_level.append(TextNode(self, compound, compound_name, compound_kind))

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

        with open("library_api.rst", "w") as generated_index:
            generated_index.write("Library API\n")
            generated_index.write("==============================================================\n\n")
            # for link_name, file_name in GENERATED_FILES:
            #     generated_index.write(
            #         ".. toctree::\n"
            #         "   :maxdepth: 1\n\n"
            #         "   {}\n\n".format(file_name)
            #     )

            for n in self.namespaces:
                generated_index.write(
                    ".. toctree::\n"
                    "   :maxdepth: 6\n\n"
                    "   {}\n\n".format(n.file_name)
                )

            # for enum, link, file, refid in namespace_enumerations:
            #     generated_index.write(
            #         ".. toctree::\n"
            #         "   :maxdepth: 1\n\n"
            #         "   {}\n\n".format(file)
            #     )

            # for enum, link, file, refid in namespace_enumerations:
            #     #NanoGUIstructarbitrary_1_1nested_1_1dual__nested_1_1int3
            #     generated_index.write("{}\n".format(enum))

            # for link in namespace_link_to_file_map:
            #     generated_index.write(
            #         "{}\n".format(namespace_link_to_file_map[link]) #, link)
            #     )

# text_root = TextRoot(breathe_root)
# for n in text_root.namespaces:
#     n.toConsole(0)

