# The Big Array Size Survey by Björkus "ThePhD" Dorkus is marked with CC0 1.0 Universal.
# To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/

import argparse
import csv
import re
import random
import matplotlib
import matplotlib.figure
import matplotlib.patheffects
import matplotlib.pylab
import matplotlib.pyplot
import numpy
import sys
import os
import math
from mpl_toolkits.basemap import Basemap
import wordcloud
import colorsys

class response:
	usage_experience_associations = {
		"": 0,
		"Unansweered": 0,
		"Recently (0 to 2 years)": 1,
		"2 to 5 years": 2,
		"5 to 10 years": 3,
		"10 to 20 years": 4,
		"20 to 30 years": 5,
		"30+ years": 6
	}
	last_use_associations = {
		"": 0,
		"Unansweered": 0,
		"Recently (0 to 2 years ago)": 1,
		"2 to 5 years ago": 2,
		"5 to 10 years ago": 3,
		"10 to 20 years ago": 4,
		"20 to 30 years ago": 5,
		"30+ years ago": 6
	}
	name_to_score_associations = {
		"Extreme Dislike (Most Hated)": -5,
		"Extreme Dislike": -5,
		"Strong Dislike": -3,
		"Minor Dislike": -1,
		"No Preference": 0,
		"Minor Like": 1,
		"Strong Like": 3,
		"Extreme Like": 5,
		"Extreme Like (Most Loved)": 5,
	}
	score_to_name_associations = {
		-5: "Extreme Dislike (Most Hated)",
		-3: "Strong Dislike",
		-1: "Minor Dislike",
		0: "No Preference",
		1: "Minor Like",
		3: "Strong Like",
		5: "Extreme Like (Most Loved)",
	}
	score_to_formatted_name_associations = {
		-5: "Extreme Dislike\n(Most Hated)",
		-3: "Strong\nDislike",
		-1: "Minor\nDislike",
		0: "No\nPreference",
		1: "Minor\nLike",
		3: "Strong\nLike",
		5: "Extreme Like\n(Most Loved)",
	}
	score_to_index_associations = {
		-5: 0,
		-3: 1,
		-1: 2,
		0: 3,
		1: 4,
		3: 5,
		5: 6
	}
	index_to_score_associations = [
		-5,
		-3,
		-1,
		0,
		1,
		3,
		5
	]
	index_to_score_name_associations = [
		"Extreme Dislike",
		"Strong Dislike",
		"Minor Dislike",
		"No Preference",
		"Minor Like",
		"Strong Like",
		"Extreme Like",
	]
	index_to_score_name_weighted_associations = [
		"Extreme Dislike (-5)",
		"Strong Dislike (-3)",
		"Minor Dislike (-1)",
		"No Preference (0)",
		"Minor Like (+1)",
		"Strong Like (+3)",
		"Extreme Like (+5)",
	]
	delivery_patterns = [
		re.compile(
			r"^\(Underscore with capital letter _Keyword; macro in a new header,\s*(.*)\)$"
		),
		re.compile(
			r"^\(Underscore with capital letter _Keyword; no macro in header,\s*(.*)\)$"
		),
		re.compile(
			r"^\(Lowercase with no underscore keyword; no macro in header,\s*(.*)\)$"
		)
	]
	index_to_delivery_associations = [
		"`_Keyword` and <stdkeyword.h>",
		"Just `_Keyword`",
		"Lowercase `keyword`"
	]
	delivery_underscore_header_index = 0
	delivery_underscore_only_index = 1
	delivery_keyword_index = 2
	spelling_patterns = [
		re.compile(r"^\(lenof \| _Lenof,\s*(.*)\)$"),
		re.compile(r"^\(lengthof \| _Lengthof,\s*(.*)\)$"),
		re.compile(r"^\(countof \| _Countof,\s*(.*)\)$"),
		re.compile(r"^\(nelemsof \| _Nelemsof,\s*(.*)\)$"),
		re.compile(r"^\(nelementsof \| _Nelementsof,\s*(.*)\)$"),
		re.compile(r"^\(extentof \| _Extentof,\s*(.*)\)$")
	]
	index_to_spelling_associations = [
		"lenof | _Lenof",
		"lengthof | _Lengthof",
		"countof | _Countof",
		"nelemsof | _Nelemsof",
		"nelementsof | _Nelementsof",
		"extentof | _Extentof"
	]
	spelling_len_index = 0
	spelling_length_index = 1
	spelling_count_index = 2
	spelling_nelems_index = 3
	spelling_nelements_index = 4
	spelling_extent_index = 5
	exact_spelling_patterns = [
		re.compile(
			r"^\(_Lengthof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Lengthof keyword; lengthof macro in ?a? new header,\s*(.*)\)$"
		),
		re.compile(
			r"^\(lengthof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Extentof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Extentof keyword; extentof macro in ?a? new header,\s*(.*)\)$"
		),
		re.compile(
			r"^\(extentof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(r"^\(_Lenof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Lenof keyword; lenof macro in ?a? new header,\s*(.*)\)$"
		),
		re.compile(r"^\(lenof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Countof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Countof keyword; countof macro in ?a? new header,\s*(.*)\)$"
		),
		re.compile(
			r"^\(countof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Nelemsof keyword; no macro in header,\s*(.*)\)$"),
		re.compile(
			r"^\(_Nelemsof keyword; nelemsof macro in ?a? new header,\s*(.*)\)$"
		),
		re.compile(
			r"^\(nelemsof keyword; no macro in header,\s*(.*)\)"),
		re.compile(
			r"^\(nelementsof keyword; no macro in header,\s*(.*)\)$")
	]
	index_to_exact_spelling_associations = [
		"_Lengthof keyword; no macro in header",
		"_Lengthof keyword; lengthof macro",
		"lengthof keyword; no macro in header",
		"_Extentof keyword; no macro in header",
		"_Extentof keyword; extentof macro",
		"extentof keyword; no macro in header",
		"_Lenof keyword; no macro in header",
		"_Lenof keyword; lenof macro",
		"lenof keyword; no macro in header",
		"_Countof keyword; no macro in header",
		"_Countof keyword; countof macro",
		"countof keyword; no macro in header",
		"_Nelemsof keyword; no macro in header",
		"_Nelemsof keyword; nelemsof macro",
		"nelemsof keyword; no macro in header",
		"nelementsof keyword; no macro in header"
	]

	def __init__(self):
		self.city_name = ""
		self.country_name = ""
		self.latitude = 0
		self.longitude = 0
		self.skill_level = ""
		self.last_use = ""
		self.usage_experience = ""
		self.id = -1
		self.delivery = [0, 0, 0]
		self.spelling = [0, 0, 0, 0, 0, 0]
		self.exact_spelling = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.comment: str | None = None

class answer_stats:
	def __init__(self, name: str):
		self.name = name
		self.mean = 0.0
		self.mode = 0.0
		self.median = 0.0 
		self.standard_deviation = 0.0
		self.standard_error = 0.0
		self.samples: list[float] = []

response_start_pattern = re.compile(
    r"==========================Response ((-)?\d+)==========================")
question_pattern = re.compile(r"^\[Question ((-)?\d+)\]$")
answer_pattern = re.compile(r"^\[Answer\]$")
lati_pattern = re.compile(r"^\[Latitude\]\s*((-)?\d+(\.?(\d*)?))$")
longi_pattern = re.compile(r"^\[(Longtitude|Longitude)\]\s*((-)?\d+(\.?(\d*)?))$")
city_pattern = re.compile(r"^\[City\]\s*(.*)$")
country_pattern = re.compile(r"^\[Country\]\s*(.*)$")
score_colors = ["slategrey", "firebrick", "gold", "limegreen", "cornflowerblue", "blueviolet", "deeppink", "cornsilk", "cyan", "fuchsia", "peachpuff", "crimson", "yellow"]
score_hatches = ["o", "x", "-", "|", "\\", "/", "*", None]

def csv_string_escape (value: str):
	value = value.replace('"', '""')
	value = value.replace("\n", r"\n")
	# not present in all CSVs but still recommended nonetheless, and less harmful than any other kind of escaping
	value = value.replace("<", r"&lt;")
	value = value.replace(">", r"&gt;")
	value = f"\"{value}\""
	return value

def make_csv_value (value: str):
	if any(x in value for x in "\"\n<>,"):
		return csv_string_escape(value)
	return value

def parse_question_answer(question_number, current_response: response,
                          line: str, line_index: int, line_count: int,
                          lines: list[str]):
	line_index += 1
	if line_index >= line_count:
		return line_index
	line = lines[line_index].strip()
	if not answer_pattern.match(line):
		return line_index
	line_index += 1
	if line_index >= line_count:
		return line_index
	line = lines[line_index].strip()
	match question_number:
		case 1:
			# discard e-mail
			pass
		case 2:
			current_response.skill_level = "Software Mentor; Professor / Teacher; Trainer" if line == "Software Mentor, Professor / Teacher, or Trainer" else line
		case 3:
			current_response.last_use = "Recently (0 to 2 years ago)" if line == "Recently (0-2 years ago)" else line
		case 4:
			current_response.usage_experience = line
		case 5:
			while line.startswith("(") and line.endswith(")"):
				for i, pat in enumerate(response.delivery_patterns):
					delivery_match = pat.match(line)
					if delivery_match:
						delivery_score = delivery_match.group(1)
						current_response.delivery[
							i] = response.name_to_score_associations[
								delivery_score]
				line_index += 1
				if line_index >= line_count:
					return line_index
				line = lines[line_index].strip()
		case 6:
			while line.startswith("(") and line.endswith(")"):
				for i, pat in enumerate(response.spelling_patterns):
					spelling_match = pat.match(line)
					if spelling_match:
						spelling_score = spelling_match.group(1)
						current_response.spelling[
							i] = response.name_to_score_associations[
								spelling_score]
				line_index += 1
				if line_index >= line_count:
					return line_index
				line = lines[line_index].strip()
		case 7:
			while line.startswith("(") and line.endswith(")"):
				for i, pat in enumerate(response.exact_spelling_patterns):
					exact_spelling_match = pat.match(line)
					if exact_spelling_match:
						exact_spelling_score = exact_spelling_match.group(1)
						current_response.exact_spelling[
							i] = response.name_to_score_associations[
								exact_spelling_score]
				line_index += 1
				if line_index >= line_count:
					return line_index
				line = lines[line_index].strip()
		case 8:
			while not line.startswith(r"==========================Response") and not line.startswith(r"-----------------------------") and not line.startswith(r"[Answer") and not line.startswith(r"[Question"):
				if current_response.comment is None:
					current_response.comment = ""
				current_response.comment += lines[line_index]
				line_index += 1
				if line_index >= line_count:
					return line_index
				line = lines[line_index].strip()
			if not current_response.comment is None:
				current_response.comment = current_response.comment.strip()
			return line_index
		case _:
			pass
	return line_index

def parse_all_counted_data(lines):
	results: list[response] = []
	current_response = None
	line_count = len(lines)
	line_index = 0
	lati_count = 0
	longi_count = 0
	while True:
		if line_index >= line_count:
			break
		line: str = lines[line_index].strip()
		if len(line) < 1:
			line_index += 1
			continue

		response_start_match = response_start_pattern.match(line)
		if response_start_match:
			id_text = response_start_match.group(1)
			current_response = response()
			current_response.id = int(id_text)
			results.append(current_response)
			line_index += 1
			continue

		if current_response is None:
			line_index += 1
			continue

		question_match = question_pattern.match(line)
		if question_match:
			question_number_text = question_match.group(1)
			question_number = int(question_number_text)
			line_index = parse_question_answer(question_number,
										current_response, line,
										line_index, line_count, lines)
			continue

		city_match = city_pattern.match(line)
		if city_match:
			city = city_match.group(1)
			current_response.city_name = city

		country_match = country_pattern.match(line)
		if country_match:
			country = country_match.group(1)
			current_response.country_name = country

		lati_match = lati_pattern.match(line)
		if lati_match:
			lati_text = lati_match.group(1)
			lati = float(lati_text)
			current_response.latitude = lati
			lati_count += 1
			if lati_count != current_response.id:
				print("something is wrong!!")

		longi_match = longi_pattern.match(line)
		if longi_match:
			longi_text = longi_match.group(2)
			longi = float(longi_text)
			current_response.longitude = longi
			longi_count += 1
			if longi_count != current_response.id:
				print("something is wrong!!")

		line_index += 1
	return results

def parse_csv_data(f):
	reader = csv.reader(f)
	results: list[response] = []
	row_index = 0
	for row in reader:
		if row_index == 0:
			row_index += 1
			continue
		result = response()
		column_index = 0
		result.id = int(row[column_index])
		column_index += 1
		result.last_use = row[column_index]
		column_index += 1
		result.usage_experience = row[column_index]
		column_index += 1
		result.skill_level = row[column_index]
		column_index += 1
		for spelling_index, _ in enumerate(result.spelling):
			spelling = int(row[column_index + spelling_index])
			result.spelling[spelling_index] = spelling
		column_index += len(result.spelling)
		for delivery_index, _ in enumerate(result.delivery):
			delivery = int(row[column_index + delivery_index])
			result.delivery[delivery_index] = delivery
		column_index += len(result.delivery)
		for exact_spelling_index, _ in enumerate(result.exact_spelling):
			exact_spelling = int(row[column_index + exact_spelling_index])
			result.exact_spelling[exact_spelling_index] = exact_spelling
		column_index += len(result.exact_spelling)
		result.comment = row[column_index]
		column_index += 1
		assert(column_index == 30)
		results.append(result)
		row_index += 1
	assert(row_index == 0 or row_index - 1 == len(results))
	return results


def write_csv_data(results : list[response], output_prefix, seed):
	with open(output_prefix + "_data.csv", "w", encoding="utf-8") as f:
		# descriptive headers
		header_line = "response_id,last_use,usage_experience,skill_level,"
		for label in response.index_to_spelling_associations:
			header_label = make_csv_value(label)
			header_line += f"{header_label},"
		for label in response.index_to_delivery_associations:
			header_label = make_csv_value(label)
			header_line += f"{header_label},"
		for label in response.index_to_exact_spelling_associations:
			header_label = make_csv_value(label)
			header_line += f"{header_label},"
		header_line += "comment\n"
		f.write(header_line)
		# rest of the data
		for result in results:
			line = f"{result.id},{make_csv_value(result.last_use)},{make_csv_value(result.usage_experience)},{make_csv_value(result.skill_level)}"
			for s in result.spelling:
				line += f",{s}"
			for d in result.delivery:
				line += f",{d}"
			for es in result.exact_spelling:
				line += f",{es}"
			line += ","
			if not result.comment is None and len(result.comment) > 0:
				comment = make_csv_value(result.comment)
				line += f"{comment}"
			line += "\n"

			f.write(line)


def draw_city_distribution(results: list[response], output_prefix, seed):
	cities_and_countries: dict[str, float] = {}
	for result in results:
		label = f"{result.city_name}"
		value = cities_and_countries.get(label, 0)
		cities_and_countries[label] = value + 1
		
	cloud = wordcloud.WordCloud(background_color="white", colormap="plasma",
					    max_words=len(cities_and_countries),
					    width=1600, height=1200,)
	cloud.generate_from_frequencies(cities_and_countries)
	img = cloud.to_image().convert("RGBA")
	for x in range(0, img.width):
		for y in range(0, img.height):
			pixel = img.getpixel((x, y))
			pixel_hsv = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
			fuzziness = 0.6
			brightness = pixel_hsv[2] / 255
			if brightness < fuzziness or pixel_hsv[1] > 0.3:
				continue
			alpha = 1.0 - ((brightness - fuzziness) / (1.0 - fuzziness))
			alpha_rgba = int(min(max(alpha * 255, 0), 255))
			img.putpixel((x, y), (pixel[0], pixel[1], pixel[2], alpha_rgba))
	img.save(output_prefix + "_cloud.png")
	matplotlib.pyplot.close('all')

def draw_map(results: list[response], output_prefix, seed):
	map = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,
	llcrnrlon=-180,urcrnrlon=180,resolution='c')
	map.drawcoastlines(color="darkblue", linewidth=0.5)
	map.fillcontinents(color="darkgreen", lake_color="royalblue")
	# draw parallels and meridians.
	map.drawparallels(numpy.arange(-90.,91.,30.), color="white", linewidth=0.5)
	map.drawmeridians(numpy.arange(-180.,181.,60.), color="white", linewidth=0.5)
	map.drawmapboundary(color="white", fill_color="royalblue")
	map.drawcountries(linewidth=0.4, color="white")
	rnd = random.Random(seed)
	markers = [".", "x", "*", "v", "d", "p"]
	colors = score_colors[:6]
	plots = []
	handles_and_labels = [None, None, None, None, None, None]
	stroke_effects = [matplotlib.patheffects.withStroke(linewidth=1.25, foreground="white")]
	
	for result in results:
		longiskew = -0.8 + (rnd.random() * 1.6)
		latiskew = -0.8 + (rnd.random() * 1.6)
		longi = result.longitude + longiskew
		lati = result.latitude + latiskew
		x, y = map(longi, lati)
		best_spelling_score_index = result.spelling.index(max(result.spelling))
		handle_label = handles_and_labels[best_spelling_score_index]
		marker = markers[best_spelling_score_index]
		marker_color = colors[best_spelling_score_index]
		plot = map.plot(x, y, marker=marker, color=(marker_color, 0.25), linewidth=0.3)
		plots.append(plot)
		if handle_label is None:
			legend_plot = map.plot(0, 0, marker=marker, color=(marker_color, 0.5), linewidth=0.30, zorder=sys.float_info.min)[0]
			plot_label = response.index_to_spelling_associations[best_spelling_score_index]
			handle_label = handles_and_labels[best_spelling_score_index] = (legend_plot, plot_label)
	
	matplotlib.pyplot.legend([hl[0] for hl in handles_and_labels], [hl[1] for hl in handles_and_labels], fontsize="x-small")
	
	title_text = matplotlib.pyplot.title("Respondent Geographic Distribution")
	title_text.set_color("#000F")
	title_text.set_path_effects(stroke_effects)
	title_text.set_fontvariant("small-caps")
	title_text.set_fontweight("bold")
	
	matplotlib.pyplot.tight_layout()
	matplotlib.pyplot.savefig(output_prefix + "_map.png", dpi=600, transparent=True)
	matplotlib.pyplot.close('all')

def draw_base_piechart(results: list[response], result_attr_string: str, output_prefix: str, seed: int, piechart_title: str, piechart_file: str, figwidth: int | None, figheight: int | None):
	label_counts: dict[str, int] = {}
	for result in results:
		result_attr = getattr(result, result_attr_string)
		if not label_counts.get(result_attr):
			label_counts[result_attr] = 0
		label_counts[result_attr] += 1

	sorted_label_counts = sorted(list(label_counts.items()), key=lambda item: item[1])
	label_counts: dict[str, int] = dict(sorted_label_counts)

	labels = [x if x != "" else "(Unanswered)" for x in label_counts]
	sizes = [label_counts[x] for x in label_counts]

	figures, axes = matplotlib.pyplot.subplots()
	if figwidth:
		figures.set_figwidth(figwidth)
	if figheight:
		figures.set_figheight(figheight)
	stroke_effects = [matplotlib.patheffects.withStroke(linewidth=2, foreground="white")]
	title_text = axes.set_title(piechart_title)
	_, texts = axes.pie(sizes, counterclock=False, labels=labels, hatch=score_hatches)

	title_text.set_fontsize(48)
	title_text.set_color("#000F")
	title_text.set_path_effects(stroke_effects)
	title_text.set_fontvariant("small-caps")
	title_text.set_fontweight("bold")
	for t in texts:
		t.set_fontsize(20)
		t.set_color("#000F")
		t.set_path_effects(stroke_effects)
	figures.savefig(piechart_file, transparent=True)
	matplotlib.pyplot.close('all')

def draw_skill_piecharts(results: list[response], output_prefix: str, seed: int):
	draw_base_piechart(results, 'skill_level', output_prefix, seed, "Respondent Skill Level", output_prefix + "_skills.png", 28, 20)

def draw_last_use_piecharts(results: list[response], output_prefix: str, seed: int):
	draw_base_piechart(results, 'last_use', output_prefix, seed, "Respondent Last Time using C", output_prefix + "_last_use.png", 21, 20)

def draw_experience_piecharts(results: list[response], output_prefix: str, seed: int):
	draw_base_piechart(results, 'usage_experience', output_prefix, seed, "Respondent Cumulative Usage Experience", output_prefix + "_experience.png", 21, 20)

def draw_base_raw_barcharts(results: list[response], raw_votes: tuple[list[int]], index_to_name_associations: list[str], chart_title: str, chart_file: str):
	stroke_effects = [matplotlib.patheffects.withStroke(linewidth=2, foreground="gainsboro")]
	figures_axes: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes] = matplotlib.pyplot.subplots()
	figures = figures_axes[0]
	axes = figures_axes[1]
	bars = []
	for i, bar_list in enumerate(raw_votes):
		bar_left_edge = -sum([x/2 if i == 3 else x for i, x in enumerate(bar_list[:4])])
		category_label_name = index_to_name_associations[i]
		for score_index, bar_score in enumerate(bar_list):
			label_name = category_label_name + ", " + response.index_to_score_name_associations[score_index]
			score_color = score_colors[score_index]
			score_marker = score_hatches[score_index]
			bar = axes.barh(i + (0.5 * i), bar_score, height=1,
			    left=bar_left_edge, color=score_color,
			    hatch=score_marker, edgecolor="navy")
			bar_left_edge += bar_score
			bar.set_label(label_name)
			bars.append(bar)
	axes.set(ylabel="", ylim=(-1, len(raw_votes) * 1.5), xlim=(-1000, 1000))
	axes.set_xlabel("\n\nRaw Vote Count", path_effects=stroke_effects, fontstyle="italic")
	axes.set_xticks(numpy.arange(-1000, 1000, 250),
			  [str(x) for x in numpy.arange(-1000, 1000, 250)],
			  path_effects=stroke_effects)
	axes.set_yticks([i * 1.5 for i, _ in enumerate(raw_votes)],
				index_to_name_associations if "|" in index_to_name_associations[0]
				else ["\n".join(s.split("; ") if ";" in s else s.split()) for s in index_to_name_associations],
				path_effects=stroke_effects)
	axes.grid(True)
	axes.legend(bars[:len(response.index_to_score_name_associations)],
		   response.index_to_score_name_associations,
		   loc="upper left", bbox_to_anchor=(1, 0.5))
	title_text = axes.set_title(chart_title)
	title_text.set_color("#000F")
	title_text.set_path_effects(stroke_effects)
	title_text.set_fontvariant("small-caps")
	title_text.set_fontweight("bold")

	figures.set_size_inches(14, 8)
	figures.tight_layout()
	figures.savefig(chart_file, transparent=True)
	matplotlib.pyplot.close('all')

def draw_base_weighted_barcharts(results: list[response], answers: tuple[answer_stats], output_prefix: str, seed: int, title: str, filename: str):
	stroke_effects = [matplotlib.patheffects.withStroke(linewidth=2, foreground="gainsboro")]
	figures_axes: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes] = matplotlib.pyplot.subplots()
	figures = figures_axes[0]
	axes = figures_axes[1]
	bars = []
	scatters = []
	rnd = random.Random(seed)
	for i, answer in enumerate(answers):
		category_label_name = answer.name
		label_name = category_label_name
		bar_color = score_colors[i % len(score_colors)]
		bar_marker = score_hatches[i % len(score_hatches)]
		y_location = i + (0.5 * i)
		bar = axes.barh(y_location, answer.mean, height=1,
			color=bar_color, hatch=bar_marker, edgecolor="navy",
			xerr=answer.standard_error, capsize=5.0)
		bar.set_label(label_name)
		bars.append(bar)
		scatter_samples_x = [x + (-0.4 + rnd.random() * 0.8) for x in answer.samples]
		scatter_samples_y = [y_location + (-0.2 + rnd.random() * 0.4) for _ in answer.samples]
		scatter = axes.scatter(scatter_samples_x, scatter_samples_y, alpha=0.005,
			color=bar_color, hatch=bar_marker, edgecolor=None)
		scatters.append(scatter)

	axes.set(ylabel="", ylim=(-1, 1.5 * len(answers)), xlim=(-6, 6))
	axes.set_xlabel("\n\nWeighted Preference Score", path_effects=stroke_effects, fontstyle="italic")
	axes.set_xticks(numpy.arange(-6, 6, 1),
			  [(str(x) + "\n" + response.score_to_formatted_name_associations[x]
			  	if x in response.score_to_formatted_name_associations
			  	else str(x))
			  for x in numpy.arange(-6, 6, 1)],
			  path_effects=stroke_effects)
	axes.set_yticks([i * 1.5 for i, _ in enumerate(answers)], [x.name for _, x in enumerate(answers)],
			  path_effects=stroke_effects)
	axes.grid(True)
	title_text = axes.set_title(title)
	title_text.set_color("#000F")
	title_text.set_path_effects(stroke_effects)
	title_text.set_fontvariant("small-caps")
	title_text.set_fontweight("bold")
	
	figures.set_size_inches(12, 6)
	figures.tight_layout()
	figures.savefig(filename, transparent=True)
	matplotlib.pyplot.close('all')

def draw_spelling_barcharts(results: list[response], output_prefix: str, seed: int):
	spelling = (
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
	)

	for result in results:
		for i, _ in enumerate(spelling):
			score = result.spelling[i]
			index = response.score_to_index_associations[score]
			spelling[i][index] += 1

	draw_base_raw_barcharts(results, spelling, response.index_to_spelling_associations, "Preferred Spelling", output_prefix + "_spelling_preference.png")

def draw_delivery_barcharts(results: list[response], output_prefix: str, seed: int):
	delivery = (
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
	)
	for result in results:
		for i, score in enumerate(delivery):
			score = result.delivery[i]
			index = response.score_to_index_associations[score]
			delivery[i][index] += 1
	draw_base_raw_barcharts(results, delivery, response.index_to_delivery_associations, "Preferred Delivery Mechanism", output_prefix + "_delivery_preference.png")

def draw_exact_spelling_barcharts(results: list[response], output_prefix: str, seed: int):
	exact_spelling = (
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
	)
	for result in results:
		for i, score in enumerate(exact_spelling):
			score = result.exact_spelling[i]
			index = response.score_to_index_associations[score]
			exact_spelling[i][index] += 1
	draw_base_raw_barcharts(results, exact_spelling, response.index_to_exact_spelling_associations, "Preferred Exact Spelling", output_prefix + "_exact_spelling_preference.png")

def draw_weighted_spelling_barcharts(results: list[response], output_prefix: str, seed: int):
	# format data
	spelling = (
		answer_stats(response.index_to_spelling_associations[0]),
		answer_stats(response.index_to_spelling_associations[1]),
		answer_stats(response.index_to_spelling_associations[2]),
		answer_stats(response.index_to_spelling_associations[3]),
		answer_stats(response.index_to_spelling_associations[4]),
		answer_stats(response.index_to_spelling_associations[5])
	)
	for result in results:
		for i, score in enumerate(spelling):
			score = result.spelling[i]
			spelling[i].samples.append(score)

	for i, answer in enumerate(spelling):
		samples = answer.samples
		answer.mean = numpy.mean(samples)
		unique_samples, unique_sample_counts = numpy.unique(samples, return_counts=True)
		answer.mode = unique_samples[numpy.argmax(unique_sample_counts)]
		answer.median = numpy.median(samples)
		answer.standard_deviation = numpy.std(samples)
		answer.standard_error = 0 if len(answer.samples) < 2 else answer.standard_deviation / math.sqrt(len(answer.samples))

	draw_base_weighted_barcharts(results, spelling, output_prefix, seed, "Weighted Preferred Spelling", output_prefix + "_weighted_spelling_preference.png")


def draw_weighted_delivery_barcharts(results: list[response], output_prefix: str, seed: int):
	delivery = (
		answer_stats(response.index_to_delivery_associations[0]),
		answer_stats(response.index_to_delivery_associations[1]),
		answer_stats(response.index_to_delivery_associations[2]),
	)
	for result in results:
		for i, score in enumerate(delivery):
			score = result.delivery[i]
			delivery[i].samples.append(score)

	for i, answer in enumerate(delivery):
		samples = answer.samples
		answer.mean = numpy.mean(samples)
		unique_samples, unique_sample_counts = numpy.unique(samples, return_counts=True)
		answer.mode = unique_samples[numpy.argmax(unique_sample_counts)]
		answer.median = numpy.median(samples)
		answer.standard_deviation = numpy.std(samples)
		answer.standard_error = 0 if len(answer.samples) < 2 else answer.standard_deviation / math.sqrt(len(answer.samples))

	draw_base_weighted_barcharts(results, delivery, output_prefix, seed, "Weighted Delivery Preference", output_prefix + "_weighted_delivery_preference.png")


def draw_weighted_exact_spelling_barcharts(results: list[response], output_prefix: str, seed: int):
	exact_spelling = (
		answer_stats(response.index_to_exact_spelling_associations[0]),
		answer_stats(response.index_to_exact_spelling_associations[1]),
		answer_stats(response.index_to_exact_spelling_associations[2]),
		answer_stats(response.index_to_exact_spelling_associations[3]),
		answer_stats(response.index_to_exact_spelling_associations[4]),
		answer_stats(response.index_to_exact_spelling_associations[5]),
		answer_stats(response.index_to_exact_spelling_associations[6]),
		answer_stats(response.index_to_exact_spelling_associations[7]),
		answer_stats(response.index_to_exact_spelling_associations[8]),
		answer_stats(response.index_to_exact_spelling_associations[9]),
		answer_stats(response.index_to_exact_spelling_associations[10]),
		answer_stats(response.index_to_exact_spelling_associations[11]),
		answer_stats(response.index_to_exact_spelling_associations[12]),
		answer_stats(response.index_to_exact_spelling_associations[13]),
		answer_stats(response.index_to_exact_spelling_associations[14]),
		answer_stats(response.index_to_exact_spelling_associations[15]),
	)
	for result in results:
		for i, score in enumerate(exact_spelling):
			score = result.exact_spelling[i]
			exact_spelling[i].samples.append(score)

	for i, answer in enumerate(exact_spelling):
		samples = answer.samples
		answer.mean = numpy.mean(samples)
		unique_samples, unique_sample_counts = numpy.unique(samples, return_counts=True)
		answer.mode = unique_samples[numpy.argmax(unique_sample_counts)]
		answer.median = numpy.median(samples)
		answer.standard_deviation = numpy.std(samples)
		answer.standard_error = 0 if len(answer.samples) < 2 else answer.standard_deviation / math.sqrt(len(answer.samples))

	draw_base_weighted_barcharts(results, exact_spelling, output_prefix, seed, "Weighted Preferred Exact Spelling", output_prefix + "_weighted_exact_spelling_preference.png")


def draw_graphs(results: list[response], output_prefix: str, seed: int):
	draw_skill_piecharts(results, output_prefix, seed)
	draw_experience_piecharts(results, output_prefix, seed)
	draw_last_use_piecharts(results, output_prefix, seed)
	draw_spelling_barcharts(results, output_prefix, seed)
	draw_delivery_barcharts(results, output_prefix, seed)
	draw_exact_spelling_barcharts(results, output_prefix, seed)
	draw_weighted_spelling_barcharts(results, output_prefix, seed)
	draw_weighted_delivery_barcharts(results, output_prefix, seed)
	draw_weighted_exact_spelling_barcharts(results, output_prefix, seed)

def main():
	arg_parser = argparse.ArgumentParser(
		prog=
		"Big Array Size Survey: https://thephd.dev/the-big-array-size-survey-for-c",
		description=
		"Parses the command line arguments to output the various bits of data.",
		epilog=
		"To learn more, see: https://thephd.dev/the-big-array-size-survey-for-c"
	)
	arg_parser.add_argument(help="Appropriately formatted input files...",
						dest="inputs",
						nargs="*")
	arg_parser.add_argument("-c", "--csv",
					help="Ignore extension and parse inputs as CSV files",
					dest="csv",
					action=argparse.BooleanOptionalAction)
	arg_parser.add_argument("-o", "--output",
					help="Output file prefix...",
					dest="output_prefix",
					default="big_array_size_survey")
	arg_parser.add_argument("-r", "--random-seed", "--random_seed",
					help="The seed to use for random number generation...",
					dest="seed",
					default=475095478549346)
	args = arg_parser.parse_args()

	survey_results = []
	allcounted_parsing = 0
	csv_parsing = 0
	for input in args.inputs:
		if (args.csv is not None and args.csv) or (os.path.splitext(input)[1] == ".csv"):
			with open(input, 'r', newline='', encoding="utf8") as f:
				survey_results.extend(parse_csv_data(f))
				csv_parsing += 1
		else:
			input_data = None
			with open(input, 'r', encoding="utf8") as f:
				input_data = f.readlines()
			survey_results.extend(parse_all_counted_data(input_data))
			allcounted_parsing += 1
			

	if allcounted_parsing > 0:
		write_csv_data(survey_results, args.output_prefix, args.seed)
		draw_map(survey_results, args.output_prefix, args.seed)
		draw_city_distribution(survey_results, args.output_prefix, args.seed)
	draw_graphs(survey_results, args.output_prefix, args.seed)

if __name__ == "__main__":
	main()
