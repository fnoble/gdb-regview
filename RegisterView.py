from xml.etree.ElementTree import ElementTree

class RegisterView:
  def load_definitions(self, defs_file):
    self.tree = ElementTree()
    self.tree.parse(defs_file)
    self.reg_defs = self.tree.getiterator('register')

  def find_registers(self, reg_name):
    regs = filter(lambda x: x.attrib['name'].startswith(reg_name), self.reg_defs)
    return map(lambda x: x.attrib['name'], regs)

  def get_reg_element(self, reg_name):
    elems = filter(lambda x: x.attrib['name'] == reg_name, self.reg_defs)
    if len(elems) > 0:
      return elems[0]
    else:
      return None

  def extract_bits(self, val, bit_len, bit_offset):
    return (val >> bit_offset) & ((1<<bit_len) - 1)

  def get_reg_address(self, name):
    return eval(self.get_reg_element(name).attrib['address'])

  def print_reg(self, name, val):
    print "%s (*0x%08X) = 0x%08X\n" % (name, self.get_reg_address(name), val)
    reg = self.get_reg_element(name)
    for field in reg.getchildren():
      bit_len = int(field.attrib['bitlength'])
      bit_offset = int(field.attrib['bitoffset'])
      bit_name = field.attrib['name']
      description = field.attrib.get('description', 'no description')
      print "%s\t0x%X\t\t%s" % (bit_name, self.extract_bits(val, bit_len, bit_offset), description)

