# Test that corpus works correctly
import dhlab as dh

class TestCorpus:
    
    def test_corpus_zero(self):
        assert len(dh.Corpus()) == 0
        
    def test_corpus(self):
        for doctype in dh.Corpus.doctypes:
            assert len(dh.Corpus(doctype=doctype, limit=2)) == 2