# utils/tech_tree_data.py
tech_tree = {
  "graph": {
    "nodes": [
      {
        "id": "milestone_lts_physics_validation",
        "label": "Milestone: LTS Tokamak Physics Validation",
        "type": "Milestone",
        "subtype": "PhysicsDemonstration",
        "trl_current": "5",
        "TRL_justification": "This milestone represents the validation of core plasma physics models in a relevant environment. The successful, high-power D-T campaigns at JET, which produced a record 69 MJ of fusion energy and tested ITER-relevant operational scenarios, constitute a clear TRL 5 achievement. This is further supported by decades of experiments on other large tokamaks and extensive validation of transport codes against experimental data. Dependency Justification (to iter_construction): The multi-billion dollar investment in ITER is predicated on the confidence gained from validating physics scaling laws on precursor machines like JET. Without these TRL 5 results, the performance of ITER would be highly uncertain.",
        "evidence": {
          "experimental_results": [
            "https://www.ipp.mpg.de/5405892/jet_rekord_2024",
            "https://ccfe.ukaea.uk/fusion-research-facility-jets-final-tritium-experiments-yield-new-energy-record/",
            "https://euro-fusion.org/eurofusion-news/dte3record/"
          ],
          "code_validation": [
            "https://pubs.aip.org/aip/pop/article/31/4/042506/3282665/Large-database-cross-verification-and-validation",
            "https://researchportalplus.anu.edu.au/en/publications/diii-d-research-advancing-the-physics-basis-for-optimizing-the-to",
            "https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2024.1380108/full"
          ]
        }
      },
      {
        "id": "milestone_iter_construction",
        "label": "Milestone: ITER Burning Plasma Demo",
        "type": "Milestone",
        "subtype": "PrototypeConstruction",
        "trl_current": "5-6",
        "TRL_justification": "ITER is a full-scale prototype system being demonstrated in a relevant environment. The fabrication and assembly of its major components (magnets, vacuum vessel) represent TRL 5 activities. The overall project, aimed at demonstrating a burning plasma (Q=10), is the definition of a TRL 6 milestone. Despite schedule delays, construction progress places its current TRL in the 5-6 range.",
        "evidence": {
          "project_status": [
            "https://www.iter.org/construction"
          ],
          "project_goals": [
            "https://www.iter.org/few-lines",
            "https://www.iter.org/node/20687/jet-beats-its-own-record"
          ]
        }
      },
      {
        "id": "concept_hts_tokamak",
        "label": "Concept: HTS Tokamak",
        "type": "ReactorConcept",
        "category": "Fusion",
        "trl_current": "4-5",
        "TRL_justification": "The TRL of this concept is gated by the TRL of its enabling technology, HTS magnets. The successful test of a large-scale 20T HTS magnet by CFS/MIT advanced the critical component to TRL 4-5. The integrated system concept is now being demonstrated through the assembly of the SPARC prototype (a TRL 4 activity), which brings the overall concept TRL to 4-5.",
        "evidence": {
          "magnet_technology_demo": [
            "https://cfs.energy/technology/hts-magnets/",
            "http://www-new.psfc.mit.edu/sparc/hts-magnet"
          ],
          "prototype_development": [
            "https://blog.cfs.energy/cfs-takes-its-next-step-toward-fusion-energy-assembling-the-sparc-tokamak/"
          ]
        }
      },
      {
        "id": "milestone_hts_magnet_demo",
        "label": "Milestone: Large-Scale HTS Magnet Demo",
        "type": "Milestone",
        "subtype": "ComponentTest",
        "trl_current": "4-5",
        "TRL_justification": "The successful 2021 test of a 20 Tesla, large-bore HTS magnet by Commonwealth Fusion Systems and MIT represents a validation of the component in a laboratory environment (TRL 4) and testing in a relevant environment that simulates fusion forces and fields (TRL 5). This milestone was the critical proof-of-principle for the HTS tokamak concept. Dependency Justification (to sparc_net_energy): The SPARC design and its predicted net-energy performance are entirely dependent on achieving the high magnetic fields made possible by this demonstrated HTS magnet technology.",
        "evidence": {
          "experimental_results": [
            "https://cfs.energy/technology/hts-magnets/",
            "http://www-new.psfc.mit.edu/sparc/hts-magnet"
          ],
          "related_rd": [
            "https://www.nature.com/articles/s41586-021-03753-3"
          ]
        }
      },
      {
        "id": "milestone_sparc_net_energy",
        "label": "Milestone: SPARC Net Energy Demo",
        "type": "Milestone",
        "subtype": "PrototypeConstruction",
        "trl_current": "4",
        "trl_projected_5_10_years": "6",
        "TRL_justification": "SPARC is the integrated system prototype for the HTS tokamak concept. As of early 2025, the project has moved into the assembly phase with the installation of the cryostat base. This represents a TRL 4 activity ('Component and/or process validation in laboratory environment,' where the 'lab' is the assembly hall). Upon successful operation and demonstration of net energy gain (Q>2), it will achieve TRL 6.",
        "evidence": {
          "project_status": [
            "https://www.world-nuclear-news.org/articles/assembly-starts-of-sparc-as-iter-cryopumps-completed",
            "https://blog.cfs.energy/cfs-takes-its-next-step-toward-fusion-energy-assembling-the-sparc-tokamak/",
            "https://cfs.energy/devens-campus/updates/"
          ]
        }
      },
      {
        "id": "concept_stellarator",
        "label": "Concept: Stellarator",
        "type": "ReactorConcept",
        "category": "Fusion",
        "trl_current": "4-5",
        "TRL_justification": "The stellarator concept's TRL is driven by the successful physics validation from the Wendelstein 7-X experiment, which demonstrated that optimized designs can achieve excellent plasma confinement, advancing the physics basis to TRL 4-5. The overall concept readiness is currently gated by the lower TRL of fabricating complex, non-planar HTS coils required for a power plant.",
        "evidence": {
          "physics_validation": [
            "https://www.iter.org/node/20687/new-records-wendelstein-7-x",
            "https://www.proximafusion.com/press-news/how-the-most-advanced-stellarator-in-the-world-set-the-stage-for-commercial-fusion",
            "https://euro-fusion.org/eurofusion-news/wendelstein-7-x-sets-world-record-for-long-plasma-triple-product/"
          ],
          "engineering_challenges": [
            "https://www.nature.com/articles/s41567-018-0141-9"
          ]
        }
      },
      {
        "id": "milestone_w7x_optimization_proof",
        "label": "Milestone: W7-X Optimized Physics Proof",
        "type": "Milestone",
        "subtype": "PhysicsDemonstration",
        "trl_current": "4-5",
        "TRL_justification": "The Wendelstein 7-X experiment has successfully demonstrated high-performance, long-pulse plasma operation, validating the physics of its computationally optimized magnetic design. It has set world records for the fusion triple product in long-pulse stellarator discharges. This constitutes validation of the concept in a lab (TRL 4) and relevant environment (TRL 5). Dependency Justification (to hts_stellarator_coil_fab): The success of W7-X provides the scientific rationale for undertaking the difficult and expensive engineering challenge of developing and fabricating complex HTS coils for a next-generation stellarator.",
        "evidence": {
          "experimental_results": [
            "https://www.iter.org/node/20687/new-records-wendelstein-7-x",
            "https://euro-fusion.org/eurofusion-news/wendelstein-7-x-sets-world-record-for-long-plasma-triple-product/"
          ]
        }
      },
      {
        "id": "milestone_hts_stellarator_coil_fab",
        "label": "Milestone: HTS Stellarator Coil Fabrication",
        "type": "Milestone",
        "subtype": "ComponentTest",
        "trl_current": "2-3",
        "trl_projected_5_10_years": "4",
        "TRL_justification": "Fabricating the complex, non-planar, high-tolerance coils for a stellarator using brittle HTS tapes is a major engineering challenge. Current R&D is at the conceptual design (TRL 2) and experimental proof-of-concept (TRL 3) stage, focusing on novel manufacturing techniques like 3D printing for small-scale prototypes. This technology is significantly less mature than HTS coils for tokamaks.",
        "evidence": {
          "research_papers": [
            "https://iopscience.iop.org/article/10.1088/1741-4326/abc7d3"
          ]
        }
      },
      {
        "id": "concept_frc",
        "label": "Concept: Field-Reversed Configuration",
        "type": "ReactorConcept",
        "category": "Fusion",
        "trl_current": "4",
        "TRL_justification": "The FRC concept has advanced to TRL 4 based on the successful demonstration of stable plasma sustainment for durations far exceeding instability growth times in laboratory experiments like C-2U. The key physics of stability has been validated, but the concept has not yet progressed to a net-energy-gain prototype.",
        "evidence": {
          "experimental_results": [
            "https://iopscience.iop.org/article/10.1088/1741-4326/aa7d7b"
          ],
          "concept_overview": [
            "https://en.wikipedia.org/wiki/Field-reversed_configuration"
          ]
        }
      },
      {
        "id": "milestone_frc_stable_sustainment",
        "label": "Milestone: FRC Stable Sustainment",
        "type": "Milestone",
        "subtype": "PhysicsDemonstration",
        "trl_current": "4",
        "TRL_justification": "Experiments at TAE Technologies (C-2U) and PPPL (PFRC) have successfully sustained FRC plasmas for many milliseconds, demonstrating stability well beyond theoretical MHD instability timescales. This validation of the stable sustainment mechanism (e.g., via neutral beams, edge biasing) in a laboratory environment constitutes a TRL 4 achievement. Dependency Justification (to frc_net_energy): Demonstrating stable sustainment is the essential prerequisite for designing and building a device intended to achieve net energy, as an unstable plasma cannot be confined long enough to reach breakeven conditions.",
        "evidence": {
          "experimental_results": [
            "https://iopscience.iop.org/article/10.1088/1741-4326/aa7d7b"
          ],
          "patents": [
            "https://patents.google.com/patent/US10515726B2"
          ]
        }
      },
      {
        "id": "milestone_frc_net_energy",
        "label": "Milestone: FRC Net Energy Demo",
        "type": "Milestone",
        "subtype": "PrototypeConstruction",
        "trl_current": "3",
        "trl_projected_5_10_years": "5",
        "TRL_justification": "The goal of achieving net energy in an FRC is currently in the design and construction phase for next-generation experimental devices by companies like Helion and TAE. The underlying technology is based on analytical studies and results from previous TRL 4 experiments, placing this milestone at TRL 3 as it moves toward component validation.",
        "evidence": {
          "company_goals": [
            "https://www.tae.com/about/news/"
          ]
        }
      },
      {
        "id": "concept_icf",
        "label": "Concept: Inertial Confinement Fusion",
        "type": "ReactorConcept",
        "category": "Fusion",
        "trl_current": "2-3",
        "TRL_justification": "The overall concept of an Inertial Fusion Energy (IFE) power plant is at a low TRL. While single-shot ignition has been achieved (TRL 5-6 milestone), the critical enabling technologies for a power plant, such as a high-repetition-rate, high-efficiency driver and automated target systems, are only at the conceptual design or early R&D stage (TRL 2-3).",
        "evidence": {
          "technology_assessments": [
            "https://www.osti.gov/biblio/1431890"
          ]
        }
      },
      {
        "id": "milestone_nif_ignition",
        "label": "Milestone: NIF Single-Shot Ignition",
        "type": "Milestone",
        "subtype": "PhysicsDemonstration",
        "trl_current": "5-6",
        "TRL_justification": "The experiments at the National Ignition Facility (NIF) that produced more fusion energy than the laser energy delivered to the target represent a successful demonstration of a prototype (the target physics) in a relevant environment (the NIF laser). This achievement of scientific breakeven and a burning plasma is a clear TRL 5-6 milestone. Dependency Justification (to ife_driver_dev): NIF's success provides the first experimental proof that ignition is possible and defines the target performance (energy, symmetry, etc.) that a future high-repetition-rate driver must be designed to deliver.",
        "evidence": {
          "experimental_results": [
            "https://lasers.llnl.gov/science/achieving-fusion-ignition",
            "https://en.wikipedia.org/wiki/National_Ignition_Facility",
            "https://sciencemediacentre.es/en/reactions-new-nuclear-fusion-milestone-us-which-could-be-first-net-gain-energy",
            "https://www.llnl.gov/article/48866/three-peer-reviewed-papers-highlight-scientific-results-national-ignition-facility-record-yield-shot"
          ]
        }
      },
      {
        "id": "milestone_ife_driver_dev",
        "label": "Milestone: IFE High-Rep-Rate Driver",
        "type": "Milestone",
        "subtype": "ComponentDevelopment",
        "trl_current": "2-3",
        "trl_projected_5_10_years": "4-5",
        "TRL_justification": "An IFE power plant requires a driver that can fire ~10-20 times per second with ~10% efficiency. This is orders of magnitude beyond the single-shot, <1% efficient NIF laser. Technologies for such drivers (e.g., diode-pumped solid-state lasers, excimer lasers) are at the conceptual design (TRL 2) and lab-scale proof-of-concept (TRL 3) stages. This represents one of the largest technology gaps for fusion energy.",
        "evidence": {
          "technology_reviews": [
            "https://www.osti.gov/biblio/1431890"
          ],
          "research_programs": [
            "https://www.energy.gov/science/articles/fusion-energy-sciences-program"
          ]
        }
      },
      {
        "id": "concept_z_pinch",
        "label": "Concept: Z-Pinch",
        "type": "ReactorConcept",
        "category": "Fusion",
        "trl_current": "4",
        "TRL_justification": "The modern Z-pinch concept, which was historically plagued by instabilities, has been advanced to TRL 4 by the successful experimental validation of sheared-flow stabilization. This physics breakthrough makes the concept viable for further development towards a reactor.",
        "evidence": {
          "concept_overview": [
            "https://en.wikipedia.org/wiki/Z-pinch",
            "https://www.zapenergy.com/how-it-works"
          ],
          "power_plant_studies": [
            "https://fti.neep.wisc.edu/fti.neep.wisc.edu/ncoe/zpinch.html"
          ]
        }
      },
      {
        "id": "milestone_sfs_z_pinch_stability",
        "label": "Milestone: Sheared-Flow Z-Pinch Stability",
        "type": "Milestone",
        "subtype": "PhysicsDemonstration",
        "trl_current": "4",
        "TRL_justification": "The ZaP experiment at the University of Washington successfully demonstrated that applying a sheared axial flow to a Z-pinch plasma can suppress the destructive instabilities that plagued early experiments. The achievement of stable quiescent periods for thousands of instability growth times constitutes a validation of this critical component/subsystem in a laboratory environment, achieving TRL 4.",
        "evidence": {
          "experimental_results": [
            "https://iopscience.iop.org/article/10.1088/0029-5515/49/7/075031"
          ],
          "company_approach": [
            "https://www.zapenergy.com/how-it-works"
          ]
        }
      },
      {
        "id": "concept_lwr_smr",
        "label": "Concept: Light Water SMR",
        "type": "ReactorConcept",
        "category": "Fission",
        "trl_current": "7-8",
        "TRL_justification": "This concept is highly mature, leveraging decades of LWR technology. The NuScale design has received Standard Design Approval from the U.S. NRC (TRL 8 for the design). First-of-a-kind commercial units are under construction in several countries (TRL 7 activity), making the overall concept readiness TRL 7-8.",
        "evidence": {
          "technology_overviews": [
            "https://www.oecd-nea.org/upload/docs/application/pdf/2021-03/7560_smr_report.pdf",
            "https://www.ansto.gov.au/news/small-modular-reactors-an-overview",
            "https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-34156.pdf"
          ]
        }
      },
      {
        "id": "milestone_lwr_smr_design_approval",
        "label": "Milestone: SMR Standard Design Approval",
        "type": "Milestone",
        "subtype": "Regulatory",
        "trl_current": "7-8",
        "TRL_justification": "NuScale Power's SMR design has received Standard Design Approval from the U.S. NRC for both its 50 MWe and 77 MWe modules. This regulatory certification signifies that the system design is complete and has been qualified against rigorous safety standards, corresponding to TRL 7-8. Dependency Justification (to lwr_smr_first_build): Design approval is a mandatory regulatory prerequisite for obtaining a license to construct and operate a commercial plant.",
        "evidence": {
          "nrc_approval": [
            "https://www.world-nuclear-news.org/articles/uprated-nuscale-smr-design-gets-us-approval",
            "https://www.utilitydive.com/news/nrc-approves-nuscale-small-modular-reactor-smr/749538/",
            "https://www.nuscalepower.com/press-releases/2025/nuscale-powers-small-modular-reactor-smr-achieves-standard-design-approval-from-us-nuclear-regulatory-commission-for-77-mwe",
            "https://www.energy.gov/ne/articles/nrc-certifies-first-us-small-modular-reactor-design"
          ]
        }
      },
      {
        "id": "milestone_lwr_smr_first_build",
        "label": "Milestone: First Commercial SMR Build",
        "type": "Milestone",
        "subtype": "CommercialDeployment",
        "trl_current": "7",
        "trl_projected_5_10_years": "9",
        "TRL_justification": "This milestone represents the 'System prototype demonstration in an operational environment'. While Russia and China have operational SMRs, the first commercial builds of Western-designed SMRs are in the construction or advanced planning stages (e.g., in China, Argentina, Canada, and the U.S.). This construction activity is TRL 7. The TRL will advance to 8 upon commissioning and 9 upon successful long-term commercial operation.",
        "evidence": {
          "global_status": [
            "https://www.world-nuclear.org/information-library/nuclear-fuel-cycle/nuclear-power-reactors/small-nuclear-power-reactors.aspx"
          ]
        }
      },
      {
        "id": "concept_htgr",
        "label": "Concept: High-Temp Gas Reactor",
        "type": "ReactorConcept",
        "category": "Fission",
        "trl_current": "6-7",
        "TRL_justification": "The HTGR concept is one of the most mature Gen-IV designs, with a long history of successful demonstration reactors. The recent commissioning and grid connection of the HTR-PM commercial demonstration plant in China elevates the concept to TRL 7. The technology is considered ready for first-of-a-kind commercial orders.",
        "evidence": {
          "technology_overviews": [
            "https://www.gen-4.org/gif/jcms/c_40465/high-temperature-gas-reactor-htgr"
          ],
          "trl_assessments": [
            "https://assets.publishing.service.gov.uk/media/610158a5e90e0703ad63350d/niro-217-r-01-issue-1-technical-assessment-of-amrs.pdf"
          ]
        }
      },
      {
        "id": "milestone_htgr_demo_reactors",
        "label": "Milestone: HTGR Demo Reactor Operation",
        "type": "Milestone",
        "subtype": "PrototypeDemonstration",
        "trl_current": "6-7",
        "TRL_justification": "Numerous HTGR demonstration reactors have been successfully operated worldwide, including prototypes in the US, UK, and Germany. Currently, Japan's HTTR and China's HTR-10 are operational research reactors (TRL 6). The commissioning and operation of China's HTR-PM commercial demonstration plant on the grid is a TRL 7 achievement.",
        "evidence": {
          "operational_history": [
            "https://en.wikipedia.org/wiki/High-temperature-gas-cooled-reactor",
            "https://www.iaea.org/sites/default/files/publications/magazines/bulletin/bull26-4/26404780510.pdf"
          ],
          "current_programs": [
            "https://www.jaea.go.jp/english/news/press/2022/090502/",
            "https://www.gov.uk/government/calls-for-evidence/potential-of-high-temperature-gas-reactors-to-support-the-amr-rd-demonstration-programme-call-for-evidence",
            "https://www.mhi.com/news/230725.html"
          ]
        }
      },
      {
        "id": "concept_msr",
        "label": "Concept: Molten Salt Reactor",
        "type": "ReactorConcept",
        "category": "Fission",
        "trl_current": "3-4",
        "TRL_justification": "The MSR concept was proven at TRL 4 by the successful operation of the Molten Salt Reactor Experiment (MSRE) in the 1960s. However, the concept has not advanced significantly since then. The primary challenges of long-term materials corrosion and chemical processing are still in the R&D and lab-scale testing phase, which constrains the overall concept TRL to the 3-4 range.",
        "evidence": {
          "technology_assessments": [
            "https://www.gen-4.org/gif/jcms/c_40471/molten-salt-reactor-msr"
          ]
        }
      },
      {
        "id": "milestone_msre_operation",
        "label": "Milestone: MSRE Proof-of-Concept",
        "type": "Milestone",
        "subtype": "PhysicsDemonstration",
        "trl_current": "4",
        "TRL_justification": "The Molten Salt Reactor Experiment (1965-1969) successfully operated for ~1.5 full-power years, demonstrating stable operation with a liquid fuel, low corrosion, and basic fuel processing. This constitutes a successful validation of the key components and integrated system in a laboratory environment, achieving TRL 4. Dependency Justification (to msr_materials_qualification): The MSRE's success proved the concept's viability, but its limited lifetime highlighted that long-term materials performance and chemistry control were the key remaining challenges that must be addressed for a commercial reactor.",
        "evidence": {
          "experimental_results": [
            "https://www.osti.gov/biblio/4030941"
          ]
        }
      },
      {
        "id": "milestone_msr_materials_qualification",
        "label": "Milestone: MSR Materials & Chemistry Control",
        "type": "Milestone",
        "subtype": "ComponentDevelopment",
        "trl_current": "3-4",
        "trl_projected_5_10_years": "5-6",
        "TRL_justification": "The key challenge for MSRs is developing and qualifying structural materials and online processing systems that can survive decades in a high-temperature, corrosive, high-radiation environment. This work is currently in the R&D phase, involving laboratory studies and analytical modeling to test new alloys and separation techniques, placing it at TRL 3-4.",
        "evidence": {
          "technology_reviews": [
            "https://www.gen-4.org/gif/jcms/c_40471/molten-salt-reactor-msr"
          ]
        }
      },
      {
        "id": "concept_sfr",
        "label": "Concept: Sodium-Cooled Fast Reactor",
        "type": "ReactorConcept",
        "category": "Fission",
        "trl_current": "5-6",
        "TRL_justification": "The SFR is the most mature fast reactor technology, with extensive global experience from the construction and operation of multiple prototype and demonstration reactors. The operation of commercial-scale plants like Russia's BN-600 and BN-800 places the technology firmly at TRL 5-6.",
        "evidence": {
          "technology_overviews": [
            "https://www.gen-4.org/resources/reports/sodium-cooled-fast-reactor-sfr-system-safety-assessment-2017",
            "https://www.oecd-nea.org/jcms/pl_46348/sodium-cooled-fast-reactor-sfr-benchmark-task-force"
          ],
          "trl_assessments": [
            "https://inldigitallibrary.inl.gov/sites/sti/sti/6721146.pdf"
          ]
        }
      },
      {
        "id": "milestone_sfr_prototype_operation",
        "label": "Milestone: SFR Prototype Reactor Operation",
        "type": "Milestone",
        "subtype": "PrototypeDemonstration",
        "trl_current": "5-6",
        "TRL_justification": "A significant number of SFR prototypes have been successfully operated worldwide, including EBR-II (USA), Phénix (France), and PFR (UK). Russia currently operates the BN-600 and BN-800 commercial prototypes, and China has commissioned the CFR-600. This extensive history of operating prototypes in a relevant power-producing environment constitutes a TRL 5-6 achievement.",
        "evidence": {
          "operational_history": [
            "https://en.wikipedia.org/wiki/Sodium-cooled_fast_reactor"
          ]
        }
      },
      {
        "id": "concept_lfr",
        "label": "Concept: Lead-Cooled Fast Reactor",
        "type": "ReactorConcept",
        "category": "Fission",
        "trl_current": "3-4",
        "TRL_justification": "The LFR concept is significantly less mature than the SFR due to major materials challenges. While some operational experience exists from Russian lead-bismuth submarine reactors, the technology for commercial power plants is still in the R&D phase, focused on materials qualification. This places the concept at TRL 3-4.",
        "evidence": {
          "technology_overviews": [
            "https://www.gen-4.org/gif/jcms/c_40479/lead-cooled-fast-reactor-lfr"
          ],
          "safety_assessments": [
            "https://www.gen-4.org/gif/upload/docs/application/pdf/2014-11/rswg_lfr_white_paper_final_8.0.pdf"
          ]
        }
      },
      {
        "id": "milestone_lfr_materials_qualification",
        "label": "Milestone: LFR Materials Qualification",
        "type": "Milestone",
        "subtype": "ComponentDevelopment",
        "trl_current": "3-4",
        "trl_projected_5_10_years": "5",
        "TRL_justification": "The primary challenge for LFRs is developing structural materials and coatings that can resist corrosion from high-temperature liquid lead. Current research is focused on lab-scale testing of advanced steels (e.g., alumina-forming austenitic steels) and coatings. This R&D activity corresponds to TRL 3-4.",
        "evidence": {
          "research_overviews": [
            "https://www.oecd-nea.org/jcms/pl_46352/lead-cooled-fast-reactor-lfr-materials-development"
          ]
        }
      },
      {
        "id": "concept_twr",
        "label": "Concept: Traveling Wave Reactor",
        "type": "ReactorConcept",
        "category": "Fission",
        "trl_current": "2-3",
        "TRL_justification": "The TWR is a conceptual design that has not been built. Its feasibility is entirely dependent on developing a fuel system that can withstand unprecedentedly high burnup and radiation damage. As this critical enabling technology is still at the basic research and conceptual design stage, the overall TWR concept is at TRL 2-3.",
        "evidence": {
          "concept_descriptions": [
            "https://en.wikipedia.org/wiki/Traveling_wave_reactor"
          ]
        }
      },
      {
        "id": "milestone_twr_fuel_qualification",
        "label": "Milestone: TWR Extreme-Burnup Fuel",
        "type": "Milestone",
        "subtype": "ComponentDevelopment",
        "trl_current": "2-3",
        "TRL_justification": "The TWR concept requires fuel to achieve burnups far exceeding any material demonstrated to date. The development of fuel and cladding that can maintain integrity under such extreme radiation damage is a fundamental materials science challenge. Current work is limited to conceptual design, modeling, and basic materials research, placing this technology at TRL 2-3.",
        "evidence": {
          "research_papers": [
            "https://experts.illinois.edu/en/publications/a-novel-approach-on-designing-ultrahigh-burnup-metallic-twr-fuels"
          ],
          "context": [
            "https://en.wikipedia.org/wiki/Traveling_wave_reactor"
          ]
        }
      },
      {
        "id": "tech_hts_magnets",
        "label": "Enabling Tech: HTS Magnets",
        "type": "EnablingTechnology",
        "trl_current": "4-5 (Tokamaks); 2-3 (Stellarators)",
        "TRL_justification": "For tokamaks, the successful test of a large-scale 20T HTS magnet by CFS/MIT validated the component in a relevant environment (TRL 4-5). For stellarators, the complex, non-planar coil geometry presents significant manufacturing challenges, and the technology is still in the R&D and small-scale prototyping phase (TRL 2-3).",
        "evidence": {
          "tokamak_magnet_demo": [
            "http://www-new.psfc.mit.edu/sparc/hts-magnet",
            "https://cfs.energy/technology/hts-magnets/"
          ],
          "stellarator_coil_rd": [
            "https://iopscience.iop.org/article/10.1088/1741-4326/abc7d3"
          ]
        }
      },
      {
        "id": "tech_triso_fuel",
        "label": "Enabling Tech: TRISO Fuel Cycle",
        "type": "EnablingTechnology",
        "trl_current": "7-8 (Fabrication); 2-3 (Processing)",
        "TRL_justification": "TRISO fuel fabrication is a mature technology (TRL 7-8), having been used in multiple demonstration reactors. However, the back-end of the fuel cycle, specifically the processing of used TRISO fuel for waste management or actinide recovery, is at a very low TRL (2-3) and has never been demonstrated at scale.",
        "evidence": {
          "fabrication_maturity": [
            "https://inis.iaea.org/records/x31tj-20847",
            "https://x-energy.com/fuel/triso-x"
          ],
          "processing_challenges": [
            "https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-32969.pdf"
          ]
        }
      },
      {
        "id": "tech_metallic_fuel",
        "label": "Enabling Tech: Metallic Fuel Cycle",
        "type": "EnablingTechnology",
        "trl_current": "6-7",
        "TRL_justification": "The metallic fuel cycle, including pyroprocessing, has been demonstrated at engineering scale with spent fuel from the EBR-II fast reactor. This successful demonstration of the integrated process in a relevant environment with actual spent fuel places the technology at TRL 6-7.",
        "evidence": {
          "trl_assessment": [
            "https://inldigitallibrary.inl.gov/sites/sti/sti/6721146.pdf"
          ],
          "program_status": [
            "https://www.anl.gov/ne/fuel-cycle-rd"
          ]
        }
      },
      {
        "id": "tech_tritium_breeding",
        "label": "Enabling Tech: Tritium Breeding Blankets",
        "type": "EnablingTechnology",
        "trl_current": "3-4",
        "TRL_justification": "Tritium breeding is essential for D-T fusion but has not yet been demonstrated in an integrated fusion environment. Several concepts are being developed as Test Blanket Modules (TBMs) for ITER. These components are currently in the design and fabrication stage (TRL 3-4) and await testing in ITER to advance to higher TRLs.",
        "evidence": {
          "iter_tbm_program": [
            "https://www.iter.org/machine/supporting-systems/tritium-breeding"
          ],
          "research_papers": [
            "https://iopscience.iop.org/article/10.1088/1741-4326/aa69e8"
          ]
        }
      },
      {
        "id": "tech_pfm",
        "label": "Enabling Tech: Plasma-Facing Materials",
        "type": "EnablingTechnology",
        "trl_current": "3-4",
        "TRL_justification": "Materials facing the plasma must withstand extreme conditions. While tungsten is the baseline for ITER, advanced materials like tungsten composites and liquid metals are needed for a power plant. These are currently being tested as samples and small components in existing devices and test stands, placing them at TRL 3-4.",
        "evidence": {
          "research_overviews": [
            "https://en.wikipedia.org/wiki/Plasma-facing_material",
            "https://www.fz-juelich.de/en/ifn/ifn-1/forschung/plasma-facing-materials"
          ]
        }
      },
      {
        "id": "tech_haleu",
        "label": "Enabling Tech: HALEU Fuel Supply",
        "type": "EnablingTechnology",
        "trl_current": "3-4 (Production)",
        "TRL_justification": "A commercial-scale HALEU supply chain is a major bottleneck for advanced fission. While the enrichment technology exists, there is no large-scale production in the West. Centrus Energy's pilot cascade in the U.S. represents a TRL 3-4 demonstration of the production process, but the full supply chain (including deconversion and transport) is less mature.",
        "evidence": {
          "supply_chain_status": [
            "https://www.energy.gov/ne/articles/what-haleu-and-why-do-we-need-it"
          ]
        }
      },
      {
        "id": "tech_power_cycle_sco2",
        "label": "Enabling Tech: sCO2 Power Cycle",
        "type": "EnablingTechnology",
        "trl_current": "5-6",
        "TRL_justification": "sCO2 Brayton cycles have been successfully tested in multiple laboratory-scale loops (TRL 5). The technology is now progressing to a 10 MWe demonstration scale at the STEP facility, which is a TRL 6 activity aimed at demonstrating the system in a relevant environment.",
        "evidence": {
          "program_overviews": [
            "https://www.energy.gov/sco2-power-cycles-nuclear",
            "https://energy.sandia.gov/programs/nuclear-energy/advanced-energy-conversion/"
          ],
          "step_project": [
            "https://sco2symposium.com/proceedings2024/59-paper.pdf"
          ]
        }
      },
      {
        "id": "milestone_step_demo_operation",
        "label": "Milestone: STEP sCO2 Demo Plant Operation",
        "type": "Milestone",
        "subtype": "PrototypeDemonstration",
        "trl_current": "6",
        "TRL_justification": "The Supercritical Transformational Electric Power (STEP) facility is a 10 MWe pilot plant designed to demonstrate sCO2 power cycle technology at a scale relevant for SMRs and other applications. Its construction and planned operation represent a TRL 6 'System/process model or prototype demonstration in a relevant environment'.",
        "evidence": {
          "program_overviews": [
            "https://www.energy.gov/sco2-power-cycles-nuclear",
            "https://sco2symposium.com/proceedings2024/59-paper.pdf"
          ]
        }
      },
      {
        "id": "tech_ai_ml_control",
        "label": "Enabling Tech: AI/ML for Control & Design",
        "type": "EnablingTechnology",
        "trl_current": "3-5",
        "TRL_justification": "The TRL is application-dependent. Using AI/ML for offline design optimization and data analysis with surrogate models is a TRL 4-5 activity. Using AI for real-time autonomous control of a nuclear reactor is less mature, currently at the algorithm development and simulation stage (TRL 3-4).",
        "evidence": {
          "applications": [
            "https://www.anl.gov/nse/ai-ml/design",
            "https://www.purdue.edu/newsroom/2024/Q2/engineers-develop-faster-more-accurate-ai-algorithm-for-improving-nuclear-reactor-performance/",
            "https://hardware.slashdot.org/story/24/08/03/0555236/could-ai-speed-up-the-design-of-nuclear-reactors"
          ]
        }
      },
      {
        "id": "tech_passive_safety",
        "label": "Enabling Tech: Passive Safety Systems",
        "type": "EnablingTechnology",
        "trl_current": "7-9 (LWRs); 4-6 (Novel Coolants)",
        "TRL_justification": "For LWRs, passive safety systems are a mature, licensed, and commercially deployed technology (e.g., AP1000), placing them at TRL 7-9. For advanced reactors with novel coolants, passive systems are a key part of the design (TRL 4-5) but require full prototype demonstration to be qualified (TRL 6).",
        "evidence": {
          "overviews": [
            "https://en.wikipedia.org/wiki/Passive_nuclear_safety",
            "https://www.numberanalytics.com/blog/passive-safety-systems-in-advanced-nuclear-reactors",
            "https://nuclearinnovationalliance.org/safety"
          ]
        }
      },
      {
        "id": "tech_rad_hard_electronics",
        "label": "Enabling Tech: Radiation-Hardened Electronics",
        "type": "EnablingTechnology",
        "trl_current": "3-7 (Application Dependent)",
        "TRL_justification": "Rad-hard electronics for established environments like space or existing nuclear plants are mature (TRL 7+). However, developing instrumentation and control systems to survive for long durations in the extreme neutron flux of a fusion core or some advanced fission concepts is a major R&D challenge, currently at TRL 3-4.",
        "evidence": {
          "technology_overviews": [
            "https://en.wikipedia.org/wiki/Radiation_hardening"
          ]
        }
      },
      {
        "id": "tech_plasma_heating",
        "label": "Enabling Tech: Plasma Heating Systems",
        "type": "EnablingTechnology",
        "trl_current": "5-6",
        "TRL_justification": "Plasma heating systems, including neutral beams and gyrotrons for ECRH, are mature technologies that have been successfully operated on all major magnetic fusion experiments for decades. They are being produced at scale for ITER, representing a technology demonstrated in a relevant environment (TRL 5-6).",
        "evidence": {
          "technology_overviews": [
            "https://www.bridge12.com/learn/nuclear-fusion-plasma-heating-and-diagnostics/"
          ]
        }
      },
      {
        "id": "tech_divertor_concepts",
        "label": "Enabling Tech: Advanced Divertor Concepts",
        "type": "EnablingTechnology",
        "trl_current": "2-3",
        "TRL_justification": "The heat fluxes in a compact fusion power plant are expected to exceed the limits of conventional solid tungsten divertors. Advanced concepts (liquid metal, snowflake, super-X) are being developed to handle these loads but are currently at the conceptual design and modeling stage (TRL 2-3).",
        "evidence": {
          "research_papers": [
            "https://iopscience.iop.org/article/10.1088/1741-4326/aa6b60"
          ]
        }
      },
      {
        "id": "milestone_advanced_divertor_test",
        "label": "Milestone: Advanced Divertor Test Facility (DTT)",
        "type": "Milestone",
        "subtype": "ComponentTest",
        "trl_current": "3",
        "TRL_justification": "The Divertor Tokamak Test (DTT) facility is being designed and constructed to test advanced divertor concepts under reactor-relevant heat and particle fluxes. As it is in the design and early construction phase, this milestone is at TRL 3.",
        "evidence": {
          "related_research": [
            "https://www.dtt-project.enea.it/"
          ]
        }
      },
      {
        "id": "concept_lts_tokamak",
        "label": "Concept: Large Tokamak (LTS)",
        "type": "ReactorConcept",
        "category": "Fusion",
        "trl_current": "5-6",
        "TRL_justification": "The large tokamak concept is represented by ITER, which is a full-scale prototype system being demonstrated in a relevant environment. The physics basis has been validated through decades of experiments on JET, DIII-D, JT-60U and other large tokamaks. ITER construction places this concept at TRL 5-6.",
        "evidence": {
          "physics_validation": [
            "https://www.iter.org/sci/Physics",
            "https://www.ipp.mpg.de/5405892/jet_rekord_2024"
          ],
          "engineering_demonstration": [
            "https://www.iter.org/construction"
          ]
        }
      }
    ],
    "edges": [
      {"id": "dep_lts_physics_to_iter", "source": "milestone_lts_physics_validation", "target": "milestone_iter_construction"},
      {"id": "dep_iter_to_tbm_test", "source": "milestone_iter_construction", "target": "tech_tritium_breeding"},
      {"id": "dep_iter_to_pfm_test", "source": "milestone_iter_construction", "target": "tech_pfm"},
      {"id": "dep_hts_tech_to_magnet_demo", "source": "tech_hts_magnets", "target": "milestone_hts_magnet_demo"},
      {"id": "dep_magnet_demo_to_sparc", "source": "milestone_hts_magnet_demo", "target": "milestone_sparc_net_energy"},
      {"id": "dep_w7x_to_hts_stellarator", "source": "milestone_w7x_optimization_proof", "target": "milestone_hts_stellarator_coil_fab"},
      {"id": "dep_hts_tech_to_stellarator_fab", "source": "tech_hts_magnets", "target": "milestone_hts_stellarator_coil_fab"},
      {"id": "dep_frc_sustain_to_net_energy", "source": "milestone_frc_stable_sustainment", "target": "milestone_frc_net_energy"},
      {"id": "dep_nif_ignition_to_ife_driver", "source": "milestone_nif_ignition", "target": "milestone_ife_driver_dev"},
      {"id": "dep_lwr_smr_approval_to_build", "source": "milestone_lwr_smr_design_approval", "target": "milestone_lwr_smr_first_build"},
      {"id": "dep_triso_fab_to_htgr_demo", "source": "tech_triso_fuel", "target": "milestone_htgr_demo_reactors"},
      {"id": "dep_haleu_to_advanced_fission", "source": "tech_haleu", "targets": ["concept_htgr", "concept_sfr", "concept_msr"]},
      {"id": "dep_msre_to_msr_materials", "source": "milestone_msre_operation", "target": "milestone_msr_materials_qualification"},
      {"id": "dep_sfr_proto_to_commercial", "source": "milestone_sfr_prototype_operation", "target": "concept_sfr"},
      {"id": "dep_metallic_fuel_to_fast_reactors", "source": "tech_metallic_fuel", "targets": ["concept_sfr", "concept_twr"]},
      {"id": "dep_sco2_tech_to_demo", "source": "tech_power_cycle_sco2", "target": "milestone_step_demo_operation"},
      {"id": "dep_sco2_demo_to_reactors", "source": "milestone_step_demo_operation", "targets": ["concept_htgr", "concept_sfr", "concept_msr", "concept_lfr"]},
      {"id": "dep_divertor_concepts_to_dtt", "source": "tech_divertor_concepts", "target": "milestone_advanced_divertor_test"},
      {"id": "dep_dtt_to_commercial_fusion", "source": "milestone_advanced_divertor_test", "targets": ["concept_hts_tokamak", "concept_stellarator"]},
      {"id": "link_iter_to_concept", "source": "milestone_iter_construction", "target": "concept_lts_tokamak"},
      {"id": "link_sparc_to_concept", "source": "milestone_sparc_net_energy", "target": "concept_hts_tokamak"},
      {"id": "link_hts_stellarator_to_concept", "source": "milestone_hts_stellarator_coil_fab", "target": "concept_stellarator"},
      {"id": "link_frc_to_concept", "source": "milestone_frc_net_energy", "target": "concept_frc"},
      {"id": "link_icf_to_concept", "source": "milestone_ife_driver_dev", "target": "concept_icf"},
      {"id": "link_z_pinch_to_concept", "source": "milestone_sfs_z_pinch_stability", "target": "concept_z_pinch"},
      {"id": "link_smr_to_concept", "source": "milestone_lwr_smr_first_build", "target": "concept_lwr_smr"},
      {"id": "link_htgr_to_concept", "source": "milestone_htgr_demo_reactors", "target": "concept_htgr"},
      {"id": "link_msr_to_concept", "source": "milestone_msr_materials_qualification", "target": "concept_msr"},
      {"id": "link_lfr_to_concept", "source": "milestone_lfr_materials_qualification", "target": "concept_lfr"},
      {"id": "link_twr_to_concept", "source": "milestone_twr_fuel_qualification", "target": "concept_twr"},
      {"id": "dep_tritium_to_fusion", "source": "tech_tritium_breeding", "targets": ["concept_lts_tokamak", "concept_hts_tokamak", "concept_stellarator"]},
      {"id": "dep_pfm_to_fusion", "source": "tech_pfm", "targets": ["concept_lts_tokamak", "concept_hts_tokamak", "concept_stellarator", "concept_frc"]},
      {"id": "dep_passive_safety_to_fission", "source": "tech_passive_safety", "targets": ["concept_lwr_smr", "concept_htgr", "concept_msr", "concept_sfr", "concept_lfr"]},
      {"id": "dep_rad_hard_to_all", "source": "tech_rad_hard_electronics", "targets": ["concept_lts_tokamak", "concept_hts_tokamak", "concept_stellarator", "concept_frc", "concept_icf", "concept_z_pinch", "concept_lwr_smr", "concept_htgr", "concept_msr", "concept_sfr", "concept_lfr", "concept_twr"]},
      {"id": "dep_plasma_heating_to_mcf", "source": "tech_plasma_heating", "targets": ["concept_lts_tokamak", "concept_hts_tokamak", "concept_stellarator", "concept_frc"]},
      {"id": "dep_ai_ml_to_all", "source": "tech_ai_ml_control", "targets": ["concept_lts_tokamak", "concept_hts_tokamak", "concept_stellarator", "concept_frc", "concept_icf", "concept_z_pinch", "concept_lwr_smr", "concept_htgr", "concept_msr", "concept_sfr", "concept_lfr", "concept_twr"]}
    ]
  }
}