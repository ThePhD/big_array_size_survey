# The Big Array Size Survey by Björkus "ThePhD" Dorkus is marked with CC0 1.0 Universal.
# To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/

import argparse
import re
import random
import matplotlib
import matplotlib.figure
import matplotlib.patheffects
import matplotlib.pylab
import matplotlib.pyplot
import numpy
import sys
from mpl_toolkits.basemap import Basemap
import wordcloud

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
		"\"_Keyword\" and <stdkeyword.h>",
		"Just \"_Keyword\"",
		"Lowercase \"keyword\""
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


response_start_pattern = re.compile(
    r"==========================Response ((-)?\d+)==========================")
question_pattern = re.compile(r"^\[Question ((-)?\d+)\]$")
answer_pattern = re.compile(r"^\[Answer\]$")
lati_pattern = re.compile(r"^\[Latitude\]\s*((-)?\d+(\.?(\d*)?))$")
longi_pattern = re.compile(r"^\[(Longtitude|Longitude)\]\s*((-)?\d+(\.?(\d*)?))$")
city_pattern = re.compile(r"^\[City\]\s*(.*)$")
country_pattern = re.compile(r"^\[Country\]\s*(.*)$")
score_colors = ["slategrey", "firebrick", "gold", "limegreen", "cornflowerblue", "blueviolet", "deeppink"]
score_hatches = ["o", "x", "-", "|", "\\", "/", "*"]
skill_hatches = ["o", "x", "-", "|", "\\", "/", "*"]

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
			current_response.skill_level = line
		case 3:
			current_response.last_use = line
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

lati_count = 0
longi_count = 0

def parse_all_counted_data_into(lines):
	results: list[response] = []
	current_response = None
	line_count = len(lines)
	line_index = 0
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
			global lati_count
			lati_count += 1
			if lati_count != current_response.id:
				print("something is wrong!!")

		longi_match = longi_pattern.match(line)
		if longi_match:
			longi_text = longi_match.group(2)
			longi = float(longi_text)
			current_response.longitude = longi
			global longi_count
			longi_count += 1
			if longi_count != current_response.id:
				print("something is wrong!!")

		line_index += 1
	return results


def write_data(results : list[response], output_prefix, seed):
	with open(output_prefix + "_data.csv", "w", encoding="utf-8") as f:
		for result in results:
			line = f"{result.id},{result.last_use},{result.skill_level}"
			for s in result.spelling:
				line += f",{s}"
			for d in result.delivery:
				line += f",{d}"
			for es in result.exact_spelling:
				line += f",{es}"
			line += ","
			if not result.comment is None and len(result.comment) > 0:
				comment = result.comment
				comment = comment.replace("\"", r"\"")
				comment = comment.replace("\\n", r"\n")
				line += f"\"{comment}\""
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
					    width=1600, height=1200)
	cloud.generate_from_frequencies(cities_and_countries)
	img = cloud.to_image().convert("RGBA")
	#for x in range(0, img.width):
	#	for y in range(0, img.height):
	#		pixel = img.getpixel((x, y))
	#		fuzziness = 40
	#		if (255 - fuzziness) <= pixel[0] <= 255 and (255 - fuzziness) <= pixel[0] <= 255 and (255 - fuzziness) <= pixel[0] <= 255:
	#			img.putpixel((x, y), (0, 0, 0, 0))
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
	map.drawmapboundary(fill_color="royalblue")
	map.drawcountries(linewidth=0.2, color="cyan")
	rnd = random.Random(seed)
	markers = [".", "x", "*", "v", "d", "p"]
	colors = score_colors[:6]
	plots = []
	handles_and_labels = [None, None, None, None, None, None]
	stroke_effects = [matplotlib.patheffects.withStroke(linewidth=1, foreground="b")]
	
	for result in results:
		longiskew = -0.8 + ((rnd.randrange(0, 100) / 100.0) * 1.6)
		latiskew = -0.8 + ((rnd.randrange(0, 100) / 100.0) * 1.6)
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
			legend_plot = map.plot(0, 0, marker=marker, color=(marker_color, 0.5), linewidth=0.3, zorder=sys.float_info.min)[0]
			plot_label = response.index_to_spelling_associations[best_spelling_score_index]
			handle_label = handles_and_labels[best_spelling_score_index] = (legend_plot, plot_label)
	
	matplotlib.pyplot.legend([hl[0] for hl in handles_and_labels], [hl[1] for hl in handles_and_labels], fontsize="x-small")
	
	title_text = matplotlib.pyplot.title("Respondent Geographic Distribution")
	title_text.set_color("#FFFF")
	title_text.set_path_effects(stroke_effects)
	
	matplotlib.pyplot.tight_layout()
	matplotlib.pyplot.savefig(output_prefix + "_map.png", dpi=600, transparent=True)
	matplotlib.pyplot.close('all')

def draw_skill_piecharts(results: list[response], output_prefix: str, seed: int):
	label_counts: dict[str, int] = {}
	for result in results:
		if not label_counts.get(result.skill_level):
			label_counts[result.skill_level] = 0
		label_counts[result.skill_level] += 1

	sorted_label_counts = sorted(list(label_counts.items()), key=lambda item: item[1])
	label_counts: dict[str, int] = dict(sorted_label_counts)

	labels = [x if x != "" else "(Unanswered)" for x in label_counts]
	sizes = [label_counts[x] for x in label_counts]

	figures, axes = matplotlib.pyplot.subplots()
	figures.set_figwidth(28)
	figures.set_figheight(20)
	stroke_effects = [matplotlib.patheffects.withStroke(linewidth=1, foreground="b")]
	title_text = axes.set_title("Respondent Skill Levels")
	_, texts = axes.pie(sizes, counterclock=False, labels=labels, hatch=skill_hatches)

	title_text.set_fontsize(48)
	title_text.set_color("#FFFF")
	title_text.set_path_effects(stroke_effects)
	for t in texts:
		t.set_fontsize(20)
		t.set_color("#FFFF")
		t.set_path_effects(stroke_effects)
	figures.savefig(output_prefix + "_skills.png", transparent=True)
	matplotlib.pyplot.close('all')

def draw_experience_piecharts(results: list[response], output_prefix: str, seed: int):
	label_counts: dict[str, int] = {}
	for result in results:
		if not label_counts.get(result.usage_experience):
			label_counts[result.usage_experience] = 0
		label_counts[result.usage_experience] += 1
	
	sorted_label_counts = sorted(list(label_counts.items()), key=lambda item: response.usage_experience_associations[item[0]])
	label_counts: dict[str, int] = dict(sorted_label_counts)

	labels = [x if x != "" else "(Unanswered)" for x in label_counts]
	sizes = [label_counts[x] for x in label_counts]

	figures, axes = matplotlib.pyplot.subplots()
	figures.set_figwidth(21)
	figures.set_figheight(20)
	stroke_effects = [matplotlib.patheffects.withStroke(linewidth=1, foreground="b")]
	title_text = axes.set_title("Respondent Usage Experience")
	_, texts = axes.pie(sizes, counterclock=False, labels=labels, hatch=score_hatches)

	title_text.set_fontsize(48)
	title_text.set_color("#FFFF")
	title_text.set_path_effects(stroke_effects)
	for t in texts:
		t.set_fontsize(20)
		t.set_color("#FFFF")
		t.set_path_effects(stroke_effects)
	figures.savefig(output_prefix + "_experience.png", transparent=True)
	matplotlib.pyplot.close('all')

def draw_spelling_barcharts(results: list[response], output_prefix: str, seed: int):
	# format data
	spelling = (
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
	)
	for result in results:
		for i, score in enumerate(spelling):
			score = result.spelling[i]
			index = response.score_to_index_associations[score]
			spelling[i][index] += 1
	figures_axes: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes] = matplotlib.pyplot.subplots()
	figures = figures_axes[0]
	axes = figures_axes[1]
	bars = []
	for i, bar_list in enumerate(spelling):
		bar_left_edge = -sum([x/2 if i == 3 else x for i, x in enumerate(bar_list[:4])])
		category_label_name = response.index_to_spelling_associations[i]
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
	axes.set(xlabel="Raw Vote Count", ylabel="", ylim=(-1, 8.5), xlim=(-1000, 1000))
	axes.set_yticks([0, 1.5, 3, 4.5, 6, 7.5], response.index_to_spelling_associations)
	axes.grid(True)
	axes.legend(bars[:len(response.index_to_score_name_associations)],
		   response.index_to_score_name_associations,
		   loc="upper left", bbox_to_anchor=(1, 0.5))
	axes.set_title("Preferred Spelling")
	figures.set_figwidth(figures.get_figwidth() * 2.8)
	figures.savefig(output_prefix + "_spelling_preference.png")
	matplotlib.pyplot.close('all')

def draw_delivery_barcharts(results: list[response], output_prefix: str, seed: int):
	# format data
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
	figures_axes: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes] = matplotlib.pyplot.subplots()
	figures = figures_axes[0]
	axes = figures_axes[1]
	bars = []
	for i, bar_list in enumerate(delivery):
		bar_left_edge = -sum([x/2 if i == 3 else x for i, x in enumerate(bar_list[:4])])
		category_label_name = response.index_to_delivery_associations[i]
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
	axes.set(xlabel="Raw Vote Count", ylabel="", ylim=(-1, 4), xlim=(-1000, 1000))
	axes.set_yticks([0, 1.5, 3], ["\n".join(s.split()) for s in response.index_to_delivery_associations])
	axes.grid(True)
	axes.legend(bars[:len(response.index_to_score_name_associations)],
		   response.index_to_score_name_associations,
		   loc="upper left", bbox_to_anchor=(1, 0.5))
	axes.set_title("Preferred Delivery Mechanism")
	figures.set_figwidth(figures.get_figwidth() * 2.8)
	figures.savefig(output_prefix + "_delivery_preference.png")
	matplotlib.pyplot.close('all')


def draw_exact_spelling_barcharts(results: list[response], output_prefix: str, seed: int):
	# format data
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
	figures_axes: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes] = matplotlib.pyplot.subplots()
	figures = figures_axes[0]
	axes = figures_axes[1]
	bars = []
	for i, bar_list in enumerate(exact_spelling):
		bar_left_edge = -sum([x/2 if i == 3 else x for i, x in enumerate(bar_list[:4])])
		category_label_name = response.index_to_exact_spelling_associations[i]
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
	axes.set(xlabel="Raw Vote Count", ylabel="", ylim=(-1, 23.5), xlim=(-1000, 1000))
	axes.set_yticks([0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12, 13.5, 15, 16.5, 18, 19.5, 21, 22.5], [";\n".join(s.split("; ")) for s in response.index_to_exact_spelling_associations])
	axes.grid(True)
	axes.legend(bars[:len(response.index_to_score_name_associations)],
		   response.index_to_score_name_associations,
		   loc="upper left", bbox_to_anchor=(1, 0.5))
	axes.set_title("Preferred Exact Spelling")
	figures.set_figwidth(figures.get_figwidth() * 2.8)
	figures.set_figheight(figures.get_figheight() * 1.8)
	figures.savefig(output_prefix + "_exact_spelling_preference.png")
	matplotlib.pyplot.close('all')


def draw_graphs(results: list[response], output_prefix: str, seed: int):
	draw_skill_piecharts(results, output_prefix, seed)
	draw_experience_piecharts(results, output_prefix, seed)
	draw_spelling_barcharts(results, output_prefix, seed)
	draw_delivery_barcharts(results, output_prefix, seed)
	draw_exact_spelling_barcharts(results, output_prefix, seed)

def main():
	arg_parser = argparse.ArgumentParser(
		prog=
		"Big Array Size Survey: https://thephd.dev/the-big-array-size-survey-for-c",
		description=
		"Parses the command line arguments to output the various bits of data.",
		epilog=
		"To learn more, see: https://thephd.dev/the-big-array-size-survey-for-c"
	)
	arg_parser.add_argument(help="AllCounted. text-formatted files...",
						dest="inputs",
						nargs="*")
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
	for input in args.inputs:
		input_data = None
		with open(input, 'r', encoding="utf8") as f:
			input_data = f.readlines()
		survey_results.extend(parse_all_counted_data_into(input_data))

	write_data(survey_results, args.output_prefix, args.seed)
	draw_map(survey_results, args.output_prefix, args.seed)
	draw_city_distribution(survey_results, args.output_prefix, args.seed)
	draw_graphs(survey_results, args.output_prefix, args.seed)

if __name__ == "__main__":
	main()
