from flask import render_template

from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_CE_RO_V1(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp
            pollingDivision = tallySheetVersion.submission.area.areaName
            if tallySheetVersion.submission.election.voteType == Postal:
                pollingDivision = 'Postal'
            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "PE/R1",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": pollingDivision,
                "data": [],
                "validVoteCount": '',
                "rejectedVoteCount": '',
                "totalVoteCount": ''
            }
            total_valid_vote_count = 0
            total_rejected_vote_count = 0
            total_vote_count = 0

            # Append the area wise column totals
            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                total_valid_vote_count += area_wise_valid_vote_count_result_item.incompleteNumValue
            content["validVoteCount"] = to_comma_seperated_num(total_valid_vote_count)
            for area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.itertuples():
                total_rejected_vote_count += area_wise_rejected_vote_count_result_item.numValue
            content["rejectedVoteCount"] = to_comma_seperated_num(total_rejected_vote_count)
            for area_wise_vote_count_result_item in area_wise_vote_count_result.itertuples():
                total_vote_count += area_wise_vote_count_result_item.incompleteNumValue
            content["totalVoteCount"] = to_comma_seperated_num(total_vote_count)

            # sort by vote count descending
            party_wise_valid_vote_count_result = party_wise_valid_vote_count_result.sort_values(
                by=['numValue'], ascending=False
            ).reset_index()

            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = [party_wise_valid_vote_count_result_item_index + 1,
                            party_wise_valid_vote_count_result_item.partyName,
                            to_comma_seperated_num(party_wise_valid_vote_count_result_item["numValue"])]
                content["data"].append(data_row)

            html = render_template(
                'PE-R1.html',
                content=content
            )

            return html


        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_and_area_wise_valid_vote_count_result = self.get_party_and_area_wise_valid_vote_count_result()
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp
            pollingDivision = tallySheetVersion.submission.area.areaName
            if tallySheetVersion.submission.election.voteType == Postal:
                pollingDivision = 'Postal'
            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "CE/RO/V1",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": pollingDivision,
                "data": [],
                "countingCentres": [],
                "validVoteCounts": [],
                "rejectedVoteCounts": [],
                "totalVoteCounts": []
            }
            total_valid_vote_count = 0
            total_rejected_vote_count = 0
            total_vote_count = 0
            # Append the area wise column totals
            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                content["countingCentres"].append(area_wise_valid_vote_count_result_item.areaName)
                content["validVoteCounts"].append(
                    to_comma_seperated_num(area_wise_valid_vote_count_result_item.incompleteNumValue))
                total_valid_vote_count += area_wise_valid_vote_count_result_item.incompleteNumValue
            for area_wise_rejected_vote_count_result_item_index, area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.iterrows():
                content["rejectedVoteCounts"].append(
                    to_comma_seperated_num(area_wise_rejected_vote_count_result_item.numValue))
                total_rejected_vote_count += area_wise_rejected_vote_count_result_item.numValue
            for area_wise_vote_count_result_item_index, area_wise_vote_count_result_item in area_wise_vote_count_result.iterrows():
                content["totalVoteCounts"].append(
                    to_comma_seperated_num(area_wise_vote_count_result_item.incompleteNumValue))
                total_vote_count += area_wise_vote_count_result_item.incompleteNumValue
            # Append the grand totals
            content["validVoteCounts"].append(to_comma_seperated_num(total_valid_vote_count))
            content["rejectedVoteCounts"].append(to_comma_seperated_num(total_rejected_vote_count))
            content["totalVoteCounts"].append(to_comma_seperated_num(total_vote_count))
            if tallySheetVersion.submission.election.voteType == Postal:
                content["tallySheetCode"] = "CE/RO/V1"
            number_of_counting_centres = len(area_wise_vote_count_result)
            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = []

                data_row_number = party_wise_valid_vote_count_result_item_index + 1
                data_row.append(data_row_number)

                data_row.append(party_wise_valid_vote_count_result_item.partyName)

                for counting_centre_index in range(number_of_counting_centres):
                    party_and_area_wise_valid_vote_count_result_item_index = \
                        (
                                number_of_counting_centres * party_wise_valid_vote_count_result_item_index) + counting_centre_index

                    data_row.append(
                        to_comma_seperated_num(party_and_area_wise_valid_vote_count_result["numValue"].values[
                                                   party_and_area_wise_valid_vote_count_result_item_index]))

                data_row.append(to_comma_seperated_num(party_wise_valid_vote_count_result_item.incompleteNumValue))

                content["data"].append(data_row)

            html = render_template(
                'PE-CE-RO-V1.html',
                content=content
            )

            return html
