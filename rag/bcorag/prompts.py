QUERY_PROMPT = "Can you give me a BioCompute Object {} domain for the provided paper. The return response must be valid JSON and must validate against the JSON schema I am providing you. {}"

USABILITY_DOMAIN = """The Usability domain in a BioCompute Object is a plain languages description
of what was done in the project or paper workflow. The Usasability domain conveys the purpose
of the Biocompute Object. The JSON schema is as follows:
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://w3id.org/ieee/ieee-2791-schema/usability_domain.json",
    "type": "array",
    "title": "Usability Domain",
    "description": "Author-defined usability domain of the IEEE-2791 Object. This field is to aid in search-ability and provide a specific description of the function of the object.",
    "items": {
        "type": "string",
        "description": "Free text values that can be used to provide scientific reasoning and purpose for the experiment",
        "examples": [
            "Identify baseline single nucleotide polymorphisms SNPs [SO:0000694], insertions [so:SO:0000667], and deletions [so:SO:0000045] that correlate with reduced ledipasvir [pubchem.compound:67505836] antiviral drug efficacy in Hepatitis C virus subtype 1 [taxonomy:31646]",
            "Identify treatment emergent amino acid substitutions [so:SO:0000048] that correlate with antiviral drug treatment failure",
            "Determine whether the treatment emergent amino acid substitutions [so:SO:0000048] identified correlate with treatment failure involving other drugs against the same virus"
        ]
    }
}
"""
