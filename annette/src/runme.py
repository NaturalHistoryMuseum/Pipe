#!/usr/bin/env python
from annette.stages.harvest import HarvestCore
from annette.stages.identify import IdentifyCore
from annette.stages.enhance import EnhanceCore
from annette.stages.classify import ClassifyCore
from annette.db import SessionManager
from datetime import datetime as dt, timedelta
from annette.db.models import ExtractedCitation, Citation
from sqlalchemy import or_
from .identify_crossref import IdentifyCrossRef

with SessionManager() as session_manager:
    # HARVEST STAGE
    extracted_citations = HarvestCore.run(session_manager)
    HarvestCore.store(session_manager, extracted_citations)
    session_manager.complete('harvest')

    # IDENTIFY STAGE
    # citations = IdentifyCore.run()
    # IdentifyCore.store(session_manager, citations)
    # session_manager.complete('identify')

    # old code -------------------------------------------------------------------------------------
    # # Set cutoff to one month before current date
    # cutoff = dt.today() - timedelta(days=31)
    #
    # # Query extractedcitation_store for records which haven't been checked against crossref
    # # in the last month (or ever)
    # mystery_extractedcitations = session_manager.session.query(ExtractedCitation).all()
    #
    # # Get bib data from crossref and update extractedcitations with confirmed DOI
    # identified_citations, id_extractedcitations = IdentifyCrossRef(
    #     mystery_extractedcitations).get_crossref_match()
    #
    # # Update extractedcitation table for both matched and unmatched extractedcitations
    # session_manager.session.add_all(id_extractedcitations)
    #
    # # Get all known citations
    # known_citations = {x.doi for x in session_manager.session.query(Citation)}
    #
    # # Strip out citations already in the database
    # identified_citations = [d for d in identified_citations if d.doi not in known_citations]
    #
    # # Add new citations
    # session_manager.session.add_all(identified_citations)
    # session_manager.session.flush()
    # print("crossref identifications written to db")
    # ----------------------------------------------------------------------------------------------

    # ENHANCE STAGE
    # metadata = EnhanceCore.run(session_manager)
    # EnhanceCore.store(session_manager, metadata)
    # session_manager.complete('enhance')

    # CLASSIFY STAGE
    updated_citations = ClassifyCore.run(session_manager)
    ClassifyCore.store(session_manager, updated_citations)
    session_manager.complete('classify')

    # ----------------------------------------------------------------------------------------------
    # if unclassified_citations:
    #     classified_citations = Classifier(unclassified_citations).classify()
    #     session.add_all(classified_citations)
    #     session.flush()
    #
    # print("classification finished starting name parsing...")
    #
    # # Extract taxonomic names (Limited to new papers)
    # nhm_citations = list(session.query(Citation)
    #     .filter(Citation.identified_date == date.today())
    #     .filter(
    #     or_(Citation.type == 'peer-review', Citation.type == 'journal-article')))
    #
    # # Get names for each title
    # result = []
    # for x in nhm_citations:
    #     result.extend(FindNames(x.doi, x.title).get_names())
    #
    # # Convert each sp. name into a Name object + write to db
    # names = [Name(doi=r[0], label=r[1], rundate=date.today()) for r in result]
    # session.add_all(names)
    # session.flush()
    #
    # # Get distinct usage key values already in Taxonomy table
    # taxonomy_keys = list(chain.from_iterable(session.query(Taxonomy.usageKey.distinct())))
    #
    # # Retrieve names in need of resolution
    # unresolved_names = list(session.query(Name).filter(Name.usage_key == None))
    #
    # #  Match names against gbif backbone
    # res_names, updated_names = ResolveName(unresolved_names).gbif_name_resolve()
    #
    # distinct_results = []
    #
    # # Get rid of duplicates
    # for n in res_names:
    #     if n.usageKey not in taxonomy_keys:
    #         distinct_results.append(n)
    #         taxonomy_keys.append(n.usageKey)
    #
    # session.add_all(updated_names)
    # session.flush()
    #
    # session.add_all(distinct_results)
    # session.flush()
    #
    # print(f"{len(distinct_results)} added to taxonomy table")
    # ----------------------------------------------------------------------------------------------

