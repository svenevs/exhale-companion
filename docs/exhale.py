__all__ = ['generate', 'TextRoot', 'TextNode']

#
# Note: known crash on struct params
#
from breathe.parser.index import parse as breathe_parse
import sys
import re
import os

EXHALE_API_TOCTREE_MAX_DEPTH = 5
'''Larger than 5 will likely produce errors with a LaTeX build, but the user can
   override this value by supplying a different value to `generate`.'''

EXHALE_API_DOXY_OUTPUT_DIR = ""

EXHALE_FILE_HEADING = "=" * 88

def generate(root_generated_directory, root_generated_file, root_generated_title,
                       root_after_title_description, root_after_body_summary, doxygen_xml_index_path,
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
        text_root = TextRoot(breathe_root, root_generated_directory, root_generated_file, root_generated_title, root_after_title_description, root_after_body_summary)
        # for n in text_root.namespaces:
        #     n.toConsole(0)


def exclaimError(msg, ascii_fmt="34;1m"):
    '''
    Prints `msg` to the console in color with ``(!) `` prepended in color.

    Example (uncolorized) output of ``exclaimError("No leading space needed.")``:

        (!) No leading space needed.

    All messages are written to `sys.stderr`, and are closed with ``[0m``.  The default
    color is blue, but can be changed using `ascii_fmt`.

    Documentation building has a verbose output process, this just helps distinguish an
    error coming from exhale.

    :type:  str
    :param: msg
    The message you want printed to standard error.

    :type:  str
    :param: ascii_fmt
    An ascii color format.  `msg` is printed as ``"\033[" + ascii_fmt + msg + "\033[0m\n``, so you
    should specify both the color code and the format code (after the semicolon).  The
    default value is ``34;1m`` --- refer to

        ``http://misc.flogisoft.com/bash/tip_colors_and_formatting``

    for alternatives.
    '''
    sys.stderr.write("\033[{}(!) {}\033[0m\n".format(ascii_fmt, msg))

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
    def __init__(self, breathe_compound):
        self.compound = breathe_compound
        self.kind     = breathe_compound.get_kind()
        self.name     = breathe_compound.get_name()
        self.refid    = breathe_compound.get_refid()
        self.children = []
        if self.kind == "file":
            self.namespaces_used = []
            self.includes        = []
            self.included_by     = [] # (refid, name) tuples for now
            self.location        = ""
            self.program_listing = []

        self.file_name = ""

    def __lt__(self, other):
        # allows alphabetical sorting within types
        if self.kind == other.kind:
            return self.name < other.name
        elif self.kind == "struct" or self.kind == "class":
            if other.kind != "struct" and other.kind != "class":
                return True
            else:
                if self.kind == "struct" and other.kind == "class":
                    return True
                elif self.kind == "class" and other.kind == "struct":
                    return False
                else:
                    return self.name < other.name
        # otherwise, sort based off the kind
        else:
            return self.kind < other.kind

    def toConsole(self, level, print_children=True):
        indent = "  " * level
        print("{}- [{}]: {}".format(indent, self.kind, self.name))
        if self.kind == "file":
            print("{}[[[ location=\"{}\" ]]]".format("  "*(level+1), self.location))
            for i in self.includes:
                print("{}- #include <{}>".format("  "*(level+1), i))
            for ref, name in self.included_by:
                print("{}- included by: [{}]".format("  "*(level+1), name))
            for n in self.namespaces_used:
                n.toConsole(level+1, print_children=False)
        if print_children:
            for c in self.children:
                c.toConsole(level+1)

    def typeSort(self):
        self.children.sort()


class TextRoot(object):
    """docstring for TextRoot"""
    def __init__(self, breathe_root, root_directory, root_file_name, root_file_title, root_file_description, root_file_summary):
        super(TextRoot, self).__init__()
        self.name = "ROOT" # used in the TextNode class


        self.breathe_root = breathe_root


        self.class_like = [] # list of TextNodes
        self.namespaces = []
        self.all_compounds = []
        self.top_level = []

        self.files = []

        # file generation location and root index data
        self.root_directory = root_directory
        self.root_file_name = root_file_name
        self.full_root_file_path = "{}/{}".format(self.root_directory, self.root_file_name)
        self.root_file_title = root_file_title
        self.root_file_description = root_file_description
        self.root_file_summary = root_file_summary


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

        # breathe directive    breathe kind
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
        # no directive     <-+-> "dir"        |
        self.dirs = []           #            |
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

        # convenience lookup
        self.node_by_refid = {}

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

        removes reparented unions
        '''
        for u in self.unions:
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
                            reparented = True
                            break

                    if reparented:
                        continue

                    # otherwise, see if it belongs to a namespace
                    alt_namespace_name = "{}::{}".format(namespace_name, potential_class)
                    for n in self.namespaces:
                        if namespace_name == n.name or alt_namespace_name == n.name:
                            n.children.append(u)
                            break
                else:
                    name_or_class_name = "::".join(p for p in parts[:-1])

                    # see if it belongs to a class like object first. if so, remove this
                    # union from the list of unions
                    reparented = False
                    for cl in self.class_like:
                        if cl.name == name_or_class_name:
                            cl.children.append(u)
                            reparented = True
                            break

                    if reparented:
                        continue

                    # next see if it belongs to a namespace
                    for n in self.namespaces:
                        if n.name == name_or_class_name:
                            n.children.append(u)
                            break

    def reparentClassLike(self):
        '''
        pass
        '''
        for cl in self.class_like:
            parts = cl.name.split("::")
            if len(parts) > 1:
                namespace_name = "::".join(parts[:-1])
                for n in self.namespaces:
                    if n.name == namespace_name:
                        n.children.append(cl)
                        break

    def reparentDirectories(self):
        dir_parts = []
        dir_ranks = []
        for d in self.dirs:
            parts = d.name.split("/")
            for p in parts:
                if p not in dir_parts:
                    dir_parts.append(p)
            dir_ranks.append((len(parts), d))

        traversal = sorted(dir_ranks)
        removals = []
        for rank, directory in reversed(traversal):
            # rank one means top level directory
            if rank < 2:
                break
            # otherwise, this is nested
            for p_rank, p_directory in reversed(traversal):
                if p_rank == rank-1:
                    if p_directory.name == "/".join(directory.name.split("/")[:-1]):
                        p_directory.children.append(directory)
                        if directory not in removals:
                            removals.append(directory)
                        break

        for rm in removals:
            self.dirs.remove(rm)

    def reparentNamespaces(self):
        '''
        pass
        '''
        namespace_parts = []
        namespace_ranks = []
        for n in self.namespaces:
            parts = n.name.split("::")
            for p in parts:
                if p not in namespace_parts:
                    namespace_parts.append(p)
            namespace_ranks.append((len(parts), n))

        traversal = sorted(namespace_ranks)
        removals = []
        for rank, namespace in reversed(traversal):
            # rank one means top level namespace
            if rank < 2:
                break
            # otherwise, this is nested
            for p_rank, p_namespace in reversed(traversal):
                if p_rank == rank-1:
                    if p_namespace.name == "::".join(namespace.name.split("::")[:-1]):
                        p_namespace.children.append(namespace)
                        if namespace not in removals:
                            removals.append(namespace)
                        break

        for rm in removals:
            self.namespaces.remove(rm)

    def renameToNamespaceScopes(self):
        '''
        Function names do not appear with the appropriate namespace prepended, so before
        we reparent the namespaces we will prepend the appropriate namespace to the
        function definition.  These will not be removed from the self.functions list.

        Same goes for variables.
        '''
        for n in self.namespaces:
            namespace_name = "{}::".format(n.name)
            for child in n.children:
                # if child.kind == "function":
                if namespace_name not in child.name:
                    child.name = "{}{}".format(namespace_name, child.name)

    def reparentAll(self):
        '''
        reparents unions to class like objects or namespaces (and removes from self.unions)

        adds classes to namespaces, but keeps the class like objects in their list
        '''
        self.reparentUnions()
        self.reparentClassLike()
        self.reparentDirectories()
        self.renameToNamespaceScopes()
        self.reparentNamespaces()

    def fileRefDiscovery(self):
        ''' Finds the missing components for files. '''
        if EXHALE_API_DOXY_OUTPUT_DIR == "":
            sys.stderr.write("(!) The doxygen xml output directory was not specified!\n")
            return
        # parse the doxygen xml file and extract all refid's put in it
        # keys: file object, values: list of refid's
        doxygen_xml_file_ownerships = {}
        # innerclass, innernamespace, etc
        ref_regex    = re.compile(r'.*<inner.*refid="(\w+)".*')
        # what files this file includes
        inc_regex    = re.compile(r'.*<includes.*>(.+)</includes>')
        # what files include this file
        inc_by_regex = re.compile(r'.*<includedby refid="(\w+)".*>(.*)</includedby>')
        # the actual location of the file
        loc_regex    = re.compile(r'.*<location file="(.*)"/>')

        for f in self.files:
            doxygen_xml_file_ownerships[f] = []
            try:
                doxy_xml_path = "{}{}.xml".format(EXHALE_API_DOXY_OUTPUT_DIR, f.refid)
                with open(doxy_xml_path, "r") as doxy_file:
                    processing_code_listing = False # shows up at bottom of xml
                    build_out_orphans       = False # one time only orphan sprawl
                    code_listing_finished   = False # use 'location' tag at bottom
                    for line in doxy_file:
                        if not processing_code_listing:
                            # gather included by references
                            match = inc_by_regex.match(line)
                            if match is not None:
                                ref, name = match.groups()
                                f.included_by.append((ref, name))
                                continue
                            # gather includes lines
                            match = inc_regex.match(line)
                            if match is not None:
                                inc = match.groups()[0]
                                f.includes.append(inc)
                                continue
                            # gather any classes, namespaces, etc declared in the file
                            match = ref_regex.match(line)
                            if match is not None:
                                match_refid = match.groups()[0]
                                if match_refid in self.node_by_refid:
                                    doxygen_xml_file_ownerships[f].append(match_refid)
                                continue
                            # lastly, see if we are starting the code listing
                            if "<programlisting>" in line:
                                processing_code_listing = True
                        else:
                            # grab the location tag while we are here
                            if code_listing_finished:
                                match = loc_regex.match(line)
                                if match is not None:
                                    f.location = match.groups()[0]
                            else:
                                if "</programlisting>" in line:
                                    code_listing_finished = True
                                else:
                                    f.program_listing.append(line)
            except:
                sys.stderr.write("Unable to process doxygen xml for file [{}].\n".format(f.name))

        # now that we have parsed all the listed refid's in the doxygen xml, reparent
        # the nodes that we care about
        for f in self.files:
            for match_refid in doxygen_xml_file_ownerships[f]:
                child = self.node_by_refid[match_refid]
                if child.kind == "struct" or child.kind == "class" or child.kind == "function" or \
                   child.kind == "typedef" or child.kind == "define" or child.kind == "enum":
                    already_there = False
                    for fc in f.children:
                        if child.name == fc.name:
                            already_there = True
                            break
                    if not already_there:
                            f.children.append(child)
                elif child.kind == "namespace":
                    already_there = False
                    for fc in f.namespaces_used:
                        if child.name == fc.name:
                            already_there = True
                            break
                    if not already_there:
                        f.namespaces_used.append(child)

        # last but not least, enums and variables declared in the file that are scoped
        # in a namespace they will show up in the programlisting, but not at the toplevel.
        for f in self.files:
            potential_orphans = []
            for n in f.namespaces_used:
                for child in n.children:
                    if child.kind == "enum" or child.kind == "variable":
                        potential_orphans.append(child)

            # now that we have a list of potential orphans, see if this doxygen xml had the
            # refid of a given child present.
            for orphan in potential_orphans:
                unresolved_name = orphan.name.split("::")[-1]
                if any(unresolved_name in line for line in f.program_listing):
                    f.children.append(orphan)

    def filePostProcess(self):
        ''' Now that each file has its location parsed from the xml, reparent to dirs '''
        removals = []
        for f in self.files:
            dir_loc_parts = f.location.split("/")[:-1]
            num_parts = len(dir_loc_parts)
            # nothing to do, at the top level
            if num_parts == 0:
                continue

            dir_path = "/".join(p for p in dir_loc_parts)
            nodes_remaining = [d for d in self.dirs]
            while len(nodes_remaining) > 0:
                d = nodes_remaining.pop()
                if d.name in dir_path:
                    # we have found the directory we want
                    if d.name == dir_path:
                        d.children.append(f)
                        removals.append(f)
                        break
                    # otherwise, try and find an owner
                    else:
                        nodes_remaining = []
                        for child in d.children:
                            if child.kind == "dir":
                                nodes_remaining.append(child)

        for rm in removals:
            self.files.remove(rm)

    def __deep_sort_list(self, lst):
        lst.sort()
        for l in lst:
            l.typeSort()

    def sortInternals(self):
        '''
        Sort mostly how doxygen would, mostly alphabetical but also hierarchical (e.g.
        structs appear before classes in listings).
        '''
        # some of the lists only need to be sorted, some of them need to be sorted and
        # have each node sort its children
        # leaf-like lists: no child sort
        self.defines.sort()
        self.enum_values.sort()
        self.functions.sort()
        self.files.sort()
        self.enums.sort()
        self.groups.sort()
        self.typedefs.sort()
        self.variables.sort()

        # hierarchical lists: sort children
        self.__deep_sort_list(self.class_like)
        self.__deep_sort_list(self.namespaces)
        self.__deep_sort_list(self.unions)

    def consoleFormat(self, section_title, lst):
        print("###########################################################")
        print("## {}".format(section_title))
        print("###########################################################")
        for l in lst:
            l.toConsole(0)

    def toConsole(self):
        self.consoleFormat("Classes and Structs", self.class_like)
        self.consoleFormat("Defines", self.defines)
        self.consoleFormat("Enums", self.enums)
        self.consoleFormat("Enum Values", self.enum_values)
        self.consoleFormat("Functions", self.functions)
        self.consoleFormat("Files", self.files)
        self.consoleFormat("Directories", self.dirs)
        self.consoleFormat("Groups", self.groups)
        self.consoleFormat("Namespaces", self.namespaces)
        self.consoleFormat("Typedefs", self.typedefs)
        self.consoleFormat("Unions", self.unions)
        self.consoleFormat("Variables", self.variables)

    def generateSingleNodeRST(self, node):
        qualifier = TextNode.qualifyKind(node.kind)
        if qualifier != "":
            qualifier = "{} : ".format(qualifier)
        else:
            print("**********************{}*******************".format(node.name))

        node.file_name = "{}/exhale_{}_{}.rst".format(self.root_directory, node.kind, node.name.replace(":", "_"))
        try:
            with open(node.file_name, "w") as gen_file:
                # generate a link label for every generated file
                link_declaration = ".. _{}:\n\n".format(node.refid)
                # every generated file must have a header for sphinx to be happy
                header = "{}\n{}\n\n".format(node.name.split("::")[-1], EXHALE_FILE_HEADING)
                # inject the appropriate doxygen directive and name of this node
                directive = ".. {}:: {}\n".format(TextNode.kindAsBreatheDirective(node.kind), node.name)
                # include any specific directives for this doxygen directive
                specifications = "{}\n\n".format(TextNode.directivesForKind(node.kind))
                gen_file.write("{}{}{}{}".format(link_declaration, header, directive, specifications))
        except:
            exclaimError("Critical error while generating the file for [{}]".format(node.file_name))

        node.file_name = node.file_name.split("/")[-1]

    def generateNodeDocuments(self):
        for cl in self.class_like:
            self.generateSingleNodeRST(cl)


    def generateViewHierarchies(self):
        pass

    def generateAPIRootHeader(self):
        try:
            if not os.path.isdir(self.root_directory):
                os.mkdir(self.root_directory)
        except Exception as e:
            exclaimError("Cannot create the directory: {}\nError message: {}".format(self.root_directory, e))
            return
        try:
            with open(self.full_root_file_path, "w") as generated_index:
                generated_index.write("{}\n{}\n\n{}\n\n".format(self.root_file_title,
                                                            EXHALE_FILE_HEADING,
                                                            self.root_file_description))
        except:
            exclaimError("Unable to create the root api file / header: {}".format(self.full_root_file_path))

    def generateAPIRootBody(self):
        try:
            with open(self.full_root_file_path, "a") as generated_index:
                for cl in self.class_like:
                    generated_index.write(
                        ".. toctree::\n"
                        "   :maxdepth: {}\n\n"
                        "   {}\n\n".format(EXHALE_API_TOCTREE_MAX_DEPTH, cl.file_name)
                    )
        except Exception as e:
            exclaimError("Unable to create the root api body: {}".format(e))

    def generateAPIRootSummary(self):
        try:
            with open(self.full_root_file_path, "a") as generated_index:
                generated_index.write("{}\n\n".format(self.root_file_summary))
        except Exception as e:
            exclaimError("Unable to create the root api summary: {}".format(e))


    def generateFullAPI(self):
        '''
        Since we are not going to use some of the breathe directives (e.g. namespace or
        file), when representing the different views of the generated API we will need:

        1. Generate a single file restructured text document for all of the nodes that
           have either no children, or children that are leaf nodes.
        2. When building the view hierarchies (class view and file view), provide a link
           to the appropriate files generated previously.

        If adding onto the framework to say add another view (from future import groups)
        you would link from a restructured text document to one of the individually
        generated files using the value of `Node.refid`.
        '''
        self.generateAPIRootHeader()
        self.generateNodeDocuments()
        self.generateViewHierarchies()
        self.generateAPIRootBody()
        self.generateAPIRootSummary()

    def __parse(self):
        for x in range(99):
            print("{}".format(x*"+"))

        self.discoverAllNodes()
        self.reparentAll()

        # now that we have all of the nodes, store them in a convenient manner for refid
        # lookup when parsing the doxygen xml files
        for n in self.all_nodes:
            self.node_by_refid[n.refid] = n

        self.fileRefDiscovery()
        self.filePostProcess()

        self.sortInternals()

        self.toConsole()

        self.generateFullAPI()








        #             #             #             #             #             #             #
        ##           ###           ###           ###           ###           ###           ##
        ###         #####         #####         #####         #####         #####         ###
        ####       #######       #######       #######       #######       #######       ####
        #####     #########     #########     #########     #########     #########     #####
        ######   ###########   ###########   ###########   ###########   ###########   ######
        ####### ############# ############# ############# ############# ############# #######
        ######   ###########   ###########   ###########   ###########   ###########   ######
        #####     #########     #########     #########     #########     #########     #####
        ####       #######       #######       #######       #######       #######       ####
        ###         #####         #####         #####         #####         #####         ###
        ##           ###           ###           ###           ###           ###           ##
        #             #             #             #             #             #             #
        #
        #
        # add in the doxygen xml parsing stuff here to get all the missing refids for files
        #
        #











        for x in range(99, 0, -1):
            print("{}".format(x*"+"))


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
