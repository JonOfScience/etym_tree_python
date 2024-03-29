"""Test operations associated with word validity pipeline"""
# import pytest
from core.core import WordField
from core.wordflow import Wordflow
from core.word import Word


class TestAnEmptyWordflowShould:
    """Test operations on a empty Wordflow"""
    def test__be_able_to_be_constructed(self):
        """State Test: Placeholder"""
        assert Wordflow()


class TestTheBaseWordFlowShould:
    """Test operations for the system default Wordflow"""
    def test__select_the_root_path_for_a_word_with_no_parents(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        orphan_word = Word()
        assert "WORD IS ROOT" in baseflow.run_stages(orphan_word)

    def test__select_the_combined_path_for_a_word_with_parents(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({"translated_word_components": ["One", "Two"]})
        assert "WORD IS COMBINED" in baseflow.run_stages(word)

    def test__pass_for_a_combined_word_that_does_not_fail_stages(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|an| + |arae|",
            "compiled_symbology": "|aba|et|an|arae|",
            "symbol_mapping": "A B C + D",
            "symbol_selection": "A C D",
            "symbol_pattern_selected": "A C + D",
            "in_language_word": "abaanarae"})
        baseflow.run_stages(word)
        assert baseflow.count_failed_stages() == 0

    def test__fail_for_a_combined_word_that_fails_translatedword_stage(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word_components": ["One", "Two"]})
        word.set_field_to(WordField.TRANSLATEDWORD, "")
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.TRANSLATEDWORD) == 1

    def test__fail_for_a_combined_word_that_fails_translated_components_stage(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["", "Two"]})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.TRANSLATEDCOMPONENTS) == 1

    def test__fail_for_a_combined_word_that_fails_in_language_components_stage(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["", "Two"]})
        baseflow.run_stages(word)
        failed_fields = baseflow.list_failed_fields()
        assert failed_fields.count(WordField.INLANGUAGECOMPONENTS) == 1

    def test__fail_for_a_combined_word_that_fails_both_etymological_symbology_stages(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba%|"})
        baseflow.run_stages(word)
        failed_fields = baseflow.list_failed_fields()
        assert failed_fields.count(WordField.ETYMOLOGICALSYMBOLOGY) == 2

    def test__fail_combined_groups_for_etymological_symbology_and_compiled_symbology(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|abaet| + |an|",
            "compiled_symbology": "|abaet|an|",
            "symbol_mapping": "A + B",
            "symbol_selection": "A B",
            "symbol_pattern_selected": "A + B",
            "in_language_word": "abaetan"})
        baseflow.run_stages(word)
        failed_fields = baseflow.list_failed_fields()
        assert len(failed_fields) == 2
        assert WordField.ETYMOLOGICALSYMBOLOGY in failed_fields
        assert WordField.COMPILEDSYMBOLOGY in failed_fields

    def test__fail_for_a_combined_word_that_fails_compiled_symbology__characters_and_sequence(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|",
            "compiled_symbology": "|ab |"})

        baseflow.run_stages(word)
        failed_fields = baseflow.list_failed_fields()
        assert failed_fields.count(WordField.COMPILEDSYMBOLOGY) == 2

    def test__fail_for_a_root_word_with_combiners(self):
        """The definition of a root word is that it is not a combination."""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": [],
            "in_language_components": [],
            "etymological_symbology": "|aba|et|",
            "compiled_symbology": "|aba|et|",
            "symbol_mapping": "A + B"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.SYMBOLMAPPING) == 1

    def test__fail_for_a_root_word_with_a_symbol_count_mismatch(self):
        """The definition of a root word is that it is not a combination."""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": [],
            "in_language_components": [],
            "etymological_symbology": "|aba|et|",
            "compiled_symbology": "|aba|et|",
            "symbol_mapping": "A B C",
            "in_language_word": "abaet"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.SYMBOLMAPPING) == 1

    def test__fail_for_a_combined_word_without_a_combiner(self):
        """The definition of a root word is that it is not a combination."""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|",
            "compiled_symbology": "|aba|et|",
            "symbol_mapping": "A B"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.SYMBOLMAPPING) == 1

    def test__fail_for_a_combined_word_with_mismatched_group_counts(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|",
            "compiled_symbology": "|aba|et|",
            "symbol_mapping": "A B + "})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.SYMBOLMAPPING) == 1

    def test__fail_for_a_combined_word_with_mismatched_individual_group_counts(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et| + |an|",
            "compiled_symbology": "|aba|et|an|",
            "symbol_mapping": "A + B"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.SYMBOLMAPPING) == 1

    def test__fail_for_a_combined_word_with_undefined_symbol(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et| + |an|",
            "compiled_symbology": "|aba|et|an|",
            "symbol_mapping": "A + B",
            "symbol_selection": "C"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.SYMBOLSELECTION) > 0
        assert baseflow.has_failure_message_like(".*Symbol Selection.*Defined Symbols.*")

    def test__fail_for_a_combined_word_with_unregistered_and_impossible_pattern(self):
        """State Test: Placeholder"""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|it| + |an|in|on|",
            "compiled_symbology": "|aba|et|it|an|in|on|",
            "symbol_mapping": "A B C + D E F",
            "symbol_selection": "A B C D E F",
            "symbol_pattern_selected": "A B C + D E F"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.SYMBOLPATTERNSELECTED) > 0
        assert baseflow.has_failure_message_like(
            ".*Symbol Pattern Selected.*Registered Selection.*")

    def test__fail_for_a_combined_word_with_mismatched_symbol_selection_and_word(self):
        """If the in_language_word does not match the symbols selected it must fail."""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|an| + |arae|",
            "compiled_symbology": "|aba|et|an|arae|",
            "symbol_mapping": "A B C + D",
            "symbol_selection": "A C D",
            "symbol_pattern_selected": "A C + D",
            "in_language_word": "abaanarai"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.INLANGUAGEWORD) > 0
        assert baseflow.has_failure_message_like(
            ".*In Language Word.*Combined Selection To In Language Word Match.*")

    def test_fail_for_a_root_word_with_mismatched_etymsymb_and_word(self):
        """If the in-language_word does not match the base combination of symbols it must fail."""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": [],
            "in_language_components": [],
            "etymological_symbology": "|aba|et|an|",
            "symbol_mapping": "A B C",
            "in_language_word": "abaetam"})
        baseflow.run_stages(word)
        assert baseflow.list_failed_fields().count(WordField.INLANGUAGEWORD) > 0
        assert baseflow.has_failure_message_like(
            ".*In Language Word.*Root Symbols To In Language Word Match.*")

    def test__contain_results_for_all_specified_stages(self):
        """Each user-defined WordField should exist at least once."""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|an| + |arae|",
            "compiled_symbology": "|aba|et|an|arae|",
            "symbol_mapping": "A B C + D",
            "symbol_selection": "A C D",
            "symbol_pattern_selected": "A C + D",
            "in_language_word": "abaanarae"})
        baseflow.run_stages(word)
        field_list = baseflow.list_stage_fields()
        assert WordField.TRANSLATEDWORD in field_list
        assert WordField.TRANSLATEDCOMPONENTS in field_list
        assert WordField.INLANGUAGECOMPONENTS in field_list
        assert WordField.ETYMOLOGICALSYMBOLOGY in field_list
        assert WordField.COMPILEDSYMBOLOGY in field_list
        assert WordField.SYMBOLMAPPING in field_list
        assert WordField.SYMBOLSELECTION in field_list
        assert WordField.SYMBOLPATTERNSELECTED in field_list
        assert WordField.INLANGUAGEWORD in field_list

    def test__contain_results_for_the_specified_stages_in_order(self):
        """Each user-defined WordField should exist in stage order."""
        baseflow = Wordflow()
        word = Word({
            "translated_word": "OneTwo",
            "translated_word_components": ["One", "Two"],
            "in_language_components": ["One", "Two"],
            "etymological_symbology": "|aba|et|an| + |arae|",
            "compiled_symbology": "|aba|et|an|arae|",
            "symbol_mapping": "A B C + D",
            "symbol_selection": "A C D",
            "symbol_pattern_selected": "A C + D",
            "in_language_word": "abaanarae"})
        baseflow.run_stages(word)
        field_list = baseflow.list_stage_fields()
        stage_pairs = {
            WordField.TRANSLATEDCOMPONENTS: WordField.TRANSLATEDWORD,
            WordField.INLANGUAGECOMPONENTS: WordField.TRANSLATEDCOMPONENTS,
            WordField.ETYMOLOGICALSYMBOLOGY: WordField.INLANGUAGECOMPONENTS,
            WordField.COMPILEDSYMBOLOGY: WordField.ETYMOLOGICALSYMBOLOGY,
            WordField.SYMBOLMAPPING: WordField.COMPILEDSYMBOLOGY,
            WordField.SYMBOLSELECTION: WordField.SYMBOLMAPPING,
            WordField.SYMBOLPATTERNSELECTED: WordField.SYMBOLSELECTION,
            WordField.INLANGUAGEWORD: WordField.SYMBOLPATTERNSELECTED}
        assert field_list[0] == WordField.TRANSLATEDWORD
        last_field = WordField.TRANSLATEDWORD
        for field in field_list[1:]:
            assert last_field in (field, stage_pairs[field])
            last_field = field
