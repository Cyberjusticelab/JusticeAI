##
# Utility used to augment the input set with synonyms.
##

from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import nltk

inputs = ['rent_change', 'lease_termination', 'deposits', 'nonpayment', 'tenant', 'landlord']

for inp in inputs:
  f = open('data/' + inp + '.txt')
  samples = set([l.strip('\n') for l in f.readlines()])

  expanded = set()
  stoppers = set(stopwords.words('english'))
  print(inp + ' old size: ' + str(len(samples)))
  while len(expanded) != len(samples):
    for sample in samples:
      sample = sample.lower()
      words = nltk.word_tokenize(sample)
      for i in words:
        if i not in stoppers:
          synsets = wn.synsets(i)
          commons = set([synset.name().split(".")[0] for synset in synsets])
          if len(commons) > 0:
            for hyponym in commons:
              newSample = sample.replace(i, hyponym.replace("_", " "))
              # print(newSample)
              expanded.add(newSample)
    samples = expanded.copy()

  # print(samples)
  print(inp + ' new size: ' + str(len(expanded)))

  out = open('data/' + inp + '.extended.txt', 'w')
  for item in expanded:
    out.write(item + '\n')