%%------------------------------------------------------------
%% General Gaia DPAC document class
%%------------------------------------------------------------
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{dpacdoc}[2006/11/15 v1.1 Gaia DPAC document class]

\LoadClass[12pt,a4paper]{article}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsbsy}
\RequirePackage{times}
\RequirePackage{ifthen}
\RequirePackage{calc}
\RequirePackage{array}
\RequirePackage{fancyhdr}
\RequirePackage{multirow}
\RequirePackage{float}
\RequirePackage{graphicx}
\RequirePackage{longtable}
\RequirePackage{eso-pic}
\RequirePackage{color}
\RequirePackage{type1cm}
\RequirePackage{hyperref}
\RequirePackage{breakurl}
\RequirePackage{natbib}
\RequirePackage{numprint}
\RequirePackage[english,iso]{isodate}
%\RequirePackage{mathptmx} % note this messes up \vec definition... do not e add put in your doc if you want it



% Switch off the onecolumn and twocolumn options
\DeclareOption{onecolumn}{\OptionNotUsed}
\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption{dpacdraft}{
    % DRAFT
    \AddToShipoutPicture{%
            \setlength{\unitlength}{0.7pt}%
        \makeatletter
            \put(\strip@pt \textwidth,\strip@pt \textheight){%
                \makebox(0,0){%
                \rotatebox{45}{%
                    \textcolor[gray]{0.95}{%
                        \fontsize{5cm}{5cm}\textsf{Draft}%
                    }}}}%
        \makeatother
    }%
}

%
% Define the various DPAC document types
%
\DeclareOption{CP}{
   \renewcommand{\dpacDocType}{Conference Proceeding}
}
\DeclareOption{MN}{
   \renewcommand{\dpacDocType}{Meeting Minutes}
}
\DeclareOption{PR}{
   \renewcommand{\dpacDocType}{Progress Report}
}
\DeclareOption{SP}{
   \renewcommand{\dpacDocType}{Specification}
}
\DeclareOption{TN}{
   \renewcommand{\dpacDocType}{Technical Note}
}
\DeclareOption{TR}{
   \renewcommand{\dpacDocType}{Test Report}
}
\DeclareOption{SDP}{
   \renewcommand{\dpacDocType}{Software Development Plan}
}
\DeclareOption{DDP}{
   \renewcommand{\dpacDocType}{Data Processing Centre Development Plan}
}
\DeclareOption{SRS}{
   \renewcommand{\dpacDocType}{Software Requirement Specifications}
}
\DeclareOption{SDD}{
   \renewcommand{\dpacDocType}{Software Design Document}
}
\DeclareOption{ICD}{
   \renewcommand{\dpacDocType}{Interface Control Document}
}
\DeclareOption{SUM}{
   \renewcommand{\dpacDocType}{Software User Manual}
}
\DeclareOption{SRN}{
   \renewcommand{\dpacDocType}{Software Release Note}
}
\DeclareOption{STP}{
   \renewcommand{\dpacDocType}{System Validation and Test Plan}
}
\DeclareOption{STS}{
   \renewcommand{\dpacDocType}{Software Test Specification}
}
\DeclareOption{STR}{
   \renewcommand{\dpacDocType}{Software Test Report}
}
\DeclareOption{VTR}{
   \renewcommand{\dpacDocType}{Validation Test Report}
}
\DeclareOption{SPAR}{
   \renewcommand{\dpacDocType}{Software Product Assurance Report}
} 
\DeclareOption{PL}{
   \renewcommand{\dpacDocType}{Planning and Policy Document}
}
\DeclareOption{UG}{
   \renewcommand{\dpacDocType}{User Guide}
}
%there is only one of these probably
\DeclareOption{SSS}{
   \renewcommand{\dpacDocType}{Software System Specification}
}  
%
% Define the CUs -- and the DPACE
%
\DeclareOption{DPACE}{
   \renewcommand{\CU}{DPACE}
}
\DeclareOption{PO}{
   \renewcommand{\CU}{PO}
}
\DeclareOption{DPx}{
   \renewcommand{\CU}{DPCx}
}
\DeclareOption{CUx}{
   \renewcommand{\CU}{CUx}
}
\DeclareOption{CU1}{
   \renewcommand{\CU}{CU1}
}
\DeclareOption{CU2}{
   \renewcommand{\CU}{CU2}
}
\DeclareOption{CU3}{
   \renewcommand{\CU}{CU3}
}
\DeclareOption{CU4}{
   \renewcommand{\CU}{CU4}
}
\DeclareOption{CU5}{
   \renewcommand{\CU}{CU5}
}
\DeclareOption{CU6}{
   \renewcommand{\CU}{CU6}
}
\DeclareOption{CU7}{
   \renewcommand{\CU}{CU7}
}
\DeclareOption{CU8}{
   \renewcommand{\CU}{CU8}
}
\DeclareOption{CU9}{
   \renewcommand{\CU}{CU9}
}
\DeclareOption{DPE}{
   \renewcommand{\CU}{DPCE}
}
\DeclareOption{DPC}{
   \renewcommand{\CU}{DPCC}
}
\DeclareOption{DPCI}{
   \renewcommand{\CU}{DPCI}
}
\DeclareOption{DPG}{
   \renewcommand{\CU}{DPCG}
}
\DeclareOption{DPT}{
   \renewcommand{\CU}{DPCT}
}
\DeclareOption{DPB}{
   \renewcommand{\CU}{DPCB}
}


%
% default settings for the newly defined commands
%
\newcommand{\setDpacDocLogo}[1]{\def\@dpacDocLogo{#1}}
\setDpacDocLogo{dpac_logo}

% you own DPC, institute or funding logo for front page
\newcommand{\setDpacDocLocalLogo}[1]{\def\@dpacDocLocalLogo{#1}}
\setDpacDocLocalLogo{}

\newcommand{\dpacDocType}{Gaia DPAC Document}
\newcommand{\CU}{CUx}

\newcommand{\DU}{}
\newcommand{\setDpacDU}[1]{\renewcommand{\DU}{-#1}}

%
% Titlepage design and macros
%
% footer title can be empty
\newsavebox{\footerTitle}
\sbox{\footerTitle}{}

\providecommand{\setDpacDocTitle}[2][@shorttitle@]{
  \def\@dpacDocTitle{\Huge #2}
  \ifthenelse{\equal{@shorttitle@}{#1}}
             {\def\@dpacDocShortTitle{}}
             {\def\@dpacDocShortTitle{#1}}
}

\newcommand{\setDpacDocSubtitle}[1]{\def\@dpacDocSubtitle{#1}
}
\setDpacDocSubtitle{}

\newcommand{\setDpacDocCompact}[1]{\def\@dpacDocCompact{#1}}
\setDpacDocCompact{}

\setDpacDocTitle{Set the document title with $\backslash$setDpacDocTitle}

\newcommand{\dpacDocDate}{set the date with {$\backslash$}setDpacDocDate}
\newcommand{\setDpacDocDate}[1]{\renewcommand{\dpacDocDate}{#1}}

\newcommand{\dpacDocIssue}{none}
\newcommand{\setDpacDocIssue}[1]{\renewcommand{\dpacDocIssue}{#1}}

\newcommand{\dpacDocStatus}{set the Status with {$\backslash$}setDpacDocStatus}
\newcommand{\setDpacDocStatus}[1]{\renewcommand{\dpacDocStatus}{#1}}

\newcommand{\dpacDocRevision}{set the Revision with {$\backslash$}setDpacDocRevision}
\newcommand{\setDpacDocRevision}[1]{\renewcommand{\dpacDocRevision}{#1}}

\newcommand{\dpacDocRef}{set the Reference with {$\backslash$}setDpacDocRef}
\newcommand{\setDpacDocRef}[1]{\renewcommand{\dpacDocRef}{#1}}

\newcommand{\dpacDocAuthor}{set the Author with {$\backslash$}setDpacDocAuthor}
\newcommand{\setDpacDocAuthor}[1]{\renewcommand{\dpacDocAuthor}{#1}}

\newcommand{\setDpacDocCurator}[1]{\def\@dpacDocCurator{#1}}
\setDpacDocCurator{}

\newcommand{\setDpacDocAffil}[1]{\def\@dpacDocAffil{#1}}
\setDpacDocAffil{}

\newcommand{\dpacDocApprove}{@noapprove@}
\newcommand{\setDpacDocApprove}[1]{\renewcommand{\dpacDocApprove}{#1}}

\newcommand{\dpacDocAuthorize}{@noauthorize@}
\newcommand{\setDpacDocAuthorize}[1]{\renewcommand{\dpacDocAuthorize}{#1}}

\newcommand{\dpacDocAbstract}{}
\newcommand{\setDpacDocAbstract}[1]{\renewcommand{\dpacDocAbstract}
{\section*{Abstract}
    \ifx \@dpacDocCompact \@empty
           \vspace*{1cm}
     \else
           \relax
    \fi
    \begin{center}
    \parbox{.9\textwidth}{#1}\\
    \end{center}
    \pagebreak
}}


\providecommand{\putlogo}{
    \ifx \@dpacDocLocalLogo \@empty
           \def\@lbsize{0.5}
     \else
           \def\@lbsize{0.75}
    \fi
  \begin{center}
   \resizebox{\@lbsize\textwidth}{!}{\includegraphics{\@dpacDocLogo}
   
    \ifx \@dpacDocLocalLogo \@empty
           \relax
     \else
           \includegraphics{\@dpacDocLocalLogo}
    \fi
   }
   \end{center}
}


\providecommand{\mkshorttitle}{
     \begin{center}
        \@dpacDocTitle \\
        \normalsize {\bf \dpacDocAuthor}\\
	Issue \dpacDocIssue.\dpacDocRevision ~~ \dpacDocDate\\
     \end{center}

}

\providecommand{\mktitle}{
   \thispagestyle{empty}
   \setlength{\parindent}{0pt}
   \vspace*{-4cm}
   \putlogo
   \centerline{\color[rgb]{0.16,0.42,0.57}}
   \rule{\textwidth}{0.5pt} \\
   \vspace*{1cm}
   \begin{center}
   \begin{minipage}{1.0\textwidth}
     \begin{center}
    \@dpacDocTitle \\
      \ifx \@dpacDocSubtitle \@empty
       \relax
    \else
         \vspace*{1cm}
         \large\@dpacDocSubtitle
    \fi
    \end{center}
   \end{minipage}
    \end{center}
   \vspace*{1cm}
   \rule{\textwidth}{0.5pt} \\[0.5cm] 
   \ifx \@dpacDocCompact \@empty
       \vspace*{2cm}
     \else
     \relax
    \fi
   {\large\textsf{
      \begin{tabbing}
         XXXXXXXXX: \=\kill
         prepared by:\> \parbox[t]{ 0.7\textwidth}{\raggedright\dpacDocAuthor}\\
    \ifx \@dpacDocAffil \@empty
     \relax
     \else
         affiliation :\> \@dpacDocAffil\\
    \fi
    \ifx \@dpacDocCurator \@empty
         \relax
         \else
         curator:\> \@dpacDocCurator\\
     \fi
    \ifthenelse{\equal{@noapprove@}{\dpacDocApprove}}%
    {}{approved by:\> \dpacDocApprove\\}%
    \ifthenelse{\equal{@noauthorize@}{\dpacDocAuthorize}}%
    {}{authorized by:\> \dpacDocAuthorize\\}%
         reference:\>   \dpacDocRef\\
\ifthenelse{\equal{\dpacDocIssue}{none}}{\relax}{%
         issue:\>       \dpacDocIssue\\}%
revision:\>    \dpacDocRevision\\
         date:\>        \dpacDocDate\\
         status:\>      \dpacDocStatus
      \end{tabbing}
   }}
   
    \ifx \@dpacDocCompact \@empty
           \pagebreak
     \else
     \relax
    \fi
   \dpacDocAbstract
}

\ProcessOptions\relax

%
%   Document history
%
\newenvironment{docHistory}[0]{
  \newpage
  \section*{Document History}
  \begin{small}
    % flush table to the left
    \setlength\LTleft{0pt}
    \setlength\LTright{\fill}
%   \setlength\LTpost{\fill}
%   \addtocounter{table}{-1}
    \begin{longtable}{|c|c|c|p{.07\textwidth}|p{.53\textwidth}|}

    \hline
    Issue & Revision & Date & Author & Comment \\ \hline\hline
}{
\end{longtable}
\end{small}
%        \ifx \@dpacDocCompact \@empty
%           \pagebreak
%         \else
%         \relax
%        \fi
}

\providecommand{\addtohist}[5]{
#1 & #2 & #3 & \path{#4} & #5\\\hline}

% 
% Issue Lists
%
\newenvironment{issueList}[0]{
\begin{longtable}{|l|p{0.8\textwidth}|}\hline \textbf{ID}&\textbf{Summary}\\\hline 
}{
\end{longtable}
}

\providecommand{\addissue}[2]{
#1 & #2\\\hline}

%
% Page layout
%
\setlength{\textwidth}{16cm}
\setlength{\textheight}{22cm}

\setlength{\topmargin}{0cm}
\setlength{\oddsidemargin}{0cm}
\setlength{\evensidemargin}{0cm}
\setlength{\leftmargini}{2cm}
\setlength{\marginparwidth}{2cm}

\setlength{\parindent}{0in}             % No indent at start of paragraphs
\setlength{\parskip}{\baselineskip}     % Blank line between paragraph

\setlength\headheight{35pt}     % Make space for logo

\pagenumbering{arabic}
\mark{{}{}} 

\newcommand{\clearemptydoublepage}{\newpage{\pagestyle{empty}\cleardoublepage}}

%% min page fraction that must be filled with text
\renewcommand{\textfraction}{0.1} 
%% max page fraction that a float may take at the top of the page
\renewcommand{\topfraction}{0.9} 
%% max page fraction that a float may take at the bottom of the page
\renewcommand{\bottomfraction}{0.9}
%% max page fraction that may be filled with floats
\renewcommand{\floatpagefraction}{0.5}
%% maximum number of floats at the top of the page
\setcounter{topnumber}{3}
%% maximum number of floats at the bottom of the page
\setcounter{bottomnumber}{1}
%% maximum total number of floats on a page
\setcounter{totalnumber}{5}

\def\fps@figure{!htbp}

\setcounter{secnumdepth}{5}    % numbering level of sections
\setcounter{tocdepth}{4}       % appearance level in table of contents

\pagestyle{fancy}

\addtolength{\headsep}{8.2mm}

\lhead{
  \IfFileExists{dpac_logo_notext.eps}{
    \resizebox{0.12\textwidth}{!}{\includegraphics{dpac_logo_notext}}
    {\bfseries\large\sf{\CU\DU}}
  } {
     \IfFileExists{dpac_logo_notext.pdf}{
       \resizebox{0.12\textwidth}{!}{\includegraphics{dpac_logo_notext}}
       {\bfseries\large\sf{\CU\DU}}
     } {
       {\bfseries\large\sf{Gaia DPAC: \CU\DU}}
       }
  }
  \vskip -1\baselineskip
}


\rhead{
 {
\begin{tabular}{l}
    \@dpacDocShortTitle \\
     {\scriptsize   \dpacDocRef }
\end{tabular}
 }
   \vskip -1\baselineskip
}


\renewcommand{\footrulewidth}{0.4pt}
\lfoot{\bfseries\sf{\dpacDocType}}
\cfoot{
\ifx \@dpacDocAffil \@empty
     \relax
     \else
        \sf \@dpacDocAffil
    \fi
}
\rfoot{\sf \thepage}

\renewcommand{\section}{\@startsection
  {section}%                                    % the name
  {1}%                                          % the level
  {0mm}%                                        % the indent
  {-10pt \@plus -1pt \@minus -1pt}%             % the beforeskip
  {4pt \@plus 1pt}%                             % the afterskip
  {\bfseries\Large}}%                           % the style
\renewcommand{\subsection}{\@startsection
  {subsection}%                                 % the name
  {2}%                                          % the level
  {0mm}%                                        % the indent
  {-5pt \@plus -1pt \@minus -1pt}%              % the beforeskip
  {2pt \@plus 1pt}%                             % the afterskip
  {\bfseries\large}}%                      % the style
\renewcommand{\subsubsection}{\@startsection
  {subsubsection}%                              % the name
  {3}%                                          % the level
  {0mm}%                                        % the indent
  {-5pt \@plus -1pt \@minus -1pt}%              % the beforeskip
  {2pt \@plus 1pt}%                             % the afterskip
  {\bfseries\normalsize}}%                      % the style


\newcommand{\gwptop}[1]{\multicolumn{1}{|l|}{\textbf{#1}}}
\newcommand{\gwpmid}[1]{\multicolumn{1}{|l|}{#1}}
\newcommand{\gwplow}[1]{\multicolumn{1}{|r|}{#1}}

\makeatother

% \renewcommand{\cite}{\citep}
\newcommand{\byte}{b}

%-----------------------------------------------------------------------------
%   Macros for dealing with requirements
%-----------------------------------------------------------------------------
\makeatletter
\nplpadding{3}
\newcounter{areqi}
\renewcommand{\theareqi}{\numprint{\arabic{areqi}}}
\def\p@areq#1{\csname reqtype\endcsname-}

% default increment for requirement counter
\providecommand{\setreqincr}[1]{\setcounter{@dfreqincr}{#1}}
\newcounter{@dfreqincr}
\setcounter{@dfreqincr}{20}

\newcounter{reqincr}
\setcounter{reqincr}{\value{@dfreqincr}}

\providecommand{\newreqtype}[1]{\def\reqtype{#1}\setcounter{areqi}{0}}

\newcounter{@reqdepth}\setcounter{@reqdepth}{0}
\newenvironment{reqblock}[2][\value{@dfreqincr}]{%
\newreqtype{#2}\setcounter{reqincr}{#1}%
\addtocounter{@reqdepth}{1}}{%
\setcounter{reqincr}{\value{@dfreqincr}}%
\addtocounter{@reqdepth}{-1}}

%
%   Requirement prefix
%
\newcommand{\reqprefix}{}
\newcommand{\setReqPrefix}[1]{\renewcommand{\reqprefix}{#1}}

%
%  requirement macro
%
\providecommand{\req}[7][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\begin{tabular}{|%
p{0\textwidth}% dummy
>{\bfseries}p{.4\textwidth}|% Req identifier
p{.11\textwidth}|% Version
%p{.11\textwidth}|% Priority
p{.22\textwidth}|% Verification
p{.11\textwidth}|% Status
}\hline%
&\csname p@areq\endcsname -\theareqi & %
 #2 &  #5 & #6\\\hline
\ifthenelse{\equal{@noparent@}{#1}}
    {& \multicolumn{4}{p{.95\textwidth}|}{#7}\\\hline}%
    {& \multicolumn{4}{p{.95\textwidth}|}{#7}\\\hline%
& \multicolumn{4}{p{.95\textwidth}|}{Parent: #1}\\\hline}%
\end{tabular}
\\[4mm]%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5}%
}

%
%   B. FREZOULS 01/13/2012
%	Applicable requirement macro
%	Created from the req command with an extra argument (the last one) 
% 	used to indicate to which system the req. is applicable
%	Display this argument in the requirement nomenclature 
% 	and add it in the log file so that the makeReqList script can add it in the Requirements.csv file
%
\providecommand{\reqapp}[8][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\begin{tabular}{|%
p{0\textwidth}% dummy
>{\bfseries}p{.4\textwidth}|% Req identifier
p{.07\textwidth}|% Version
%p{.11\textwidth}|% Priority
p{.07\textwidth}|% Verification
p{.11\textwidth}|% Status
p{.19\textwidth}|% Applicability
}\hline%
&\csname p@areq\endcsname -\theareqi & %
 #2 &  #5 & #6 & #7\\\hline
\ifthenelse{\equal{@noparent@}{#1}}
    {& \multicolumn{5}{p{.95\textwidth}|}{#8}\\\hline}%
    {& \multicolumn{5}{p{.95\textwidth}|}{#8}\\\hline%
& \multicolumn{5}{p{.95\textwidth}|}{Parent: #1}\\\hline}%
\end{tabular}
\\[4mm]%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5,#7}%
}

%   B. FREZOULS 01/18/2012
%	Deleted requirement macro
%	Created from the req command
% 	used to 'create' deleted requirement.
% 	The requirement is not displayed in the PDF produced but it exists i.e. it is listed 
% 	in the Requirements.csv file produced by the makeReqList.rb.
%	This requirement does not 'break' the numbering schema i.e. the requirements following the requirement
%	deleted keep their number/name 
%
\providecommand{\reqdel}[7][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
%\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5}%
}

%   B. FREZOULS 01/18/2012
%	Deleted requirement macro
%	Created from the reqapp command
% 	used to 'create' deleted requirement.
% 	The requirement is not displayed in the PDF produced but it exists i.e. it is listed 
% 	in the Requirements.csv file produced by the makeReqList.rb.
%	This requirement does not 'break' the numbering schema i.e. the requirements following the requirement
%	deleted keep their number/name 
%
\providecommand{\reqdel}[8][@noparent@]{%
\addtocounter{areqi}{\value{reqincr}}%
\protected@edef\@currentlabel{\csname p@areq\endcsname-\theareqi}%
\typeout{REQ:\reqprefix\csname p@areq\endcsname-\arabic{areqi},#2,#1,#6,#5,#7}%
}


\def\defsavectr#1#2#3{%
  \expandafter\edef\csname#1#2\endcsname{#3}%
}
\newcounter{@checkreq}
\newenvironment{reqinsert}[2][\value{@dfreqincr}]{\mbox{}%
\defsavectr{@savectr}{\romannumeral\value{@reqdepth}}{\arabic{areqi}}%
\defsavectr{@saveinc}{\romannumeral\value{@reqdepth}}{\thereqincr}%
\addtocounter{@reqdepth}{1}%
\setcounter{reqincr}{#1}%
}{%
\addtocounter{@reqdepth}{-1}%
\setcounter{reqincr}{\csname @saveinc\romannumeral\the@reqdepth\endcsname}%
\setcounter{@checkreq}{\csname @savectr\romannumeral\the@reqdepth\endcsname+\value{reqincr}}%
\ifthenelse{\value{@checkreq}<\value{areqi}}{\errmessage{Requirement numbering incorrect: \the@checkreq<\arabic{areqi}}}{}%
\setcounter{areqi}{\csname @savectr\romannumeral\the@reqdepth\endcsname}}
\makeatother

%
%   requirement status labels
%
\providecommand{\reqiss}{Issued} % Issued requirements
\providecommand{\reqobs}{Obsolete} % Obsolete requirements
\providecommand{\reqdel}{Deleted} % Deleted requirements

% -----------------------------------------------------------------------------
% Meeting action management
% -----------------------------------------------------------------------------
\makeatletter
\newcommand{\actprefix}{}
\newcommand{\setActionItemPrefix}[1]{\renewcommand{\actprefix}{#1}}

\newcounter{aacti}
\setcounter{aacti}{0}
\renewcommand{\theaacti}{\nplpadding{2}\numprint{\arabic{aacti}}}

\newboolean{@actstarted}
\setboolean{@actstarted}{false}
\newboolean{@oldactstarted}
\setboolean{@oldactstarted}{false}


% AI in the margin
\newcommand\marginlabel[1]{\mbox{}\marginpar{\raggedright\hspace{0pt}#1}}

% the actual action macro
% altered DWE 19/6/2008 to introduce \oldaction and \nolabelaction
%   also added hyperlinks between the actions and the action table
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\action}[3]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@actstarted}}{\relax}{\immediate\openout7=actions\setboolean{@actstarted}{true}}
\addtocounter{aacti}{1}
\immediate\write7{\noexpand\hypertarget{\actprefix\arabic{aacti}}{\actprefix\arabic{aacti}} &
        #1 & #2 & #3\string\\\noexpand\hline}

%\vspace{-1\textheight} % does not work
\vspace{-28pt}\marginlabel{AI \hyperlink{\actprefix\arabic{aacti}}{\actprefix\arabic{aacti}}}%

\typeout{AI:\actprefix\arabic{aacti},#1,#2,#3}%
}

% the actual nolabelaction macro
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\nolabelaction}[3]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@actstarted}}{\relax}{\immediate\openout7=actions\setboolean{@actstarted}{true}}
\addtocounter{aacti}{1}
\immediate\write7{\actprefix\arabic{aacti} & #1 & #2 & #3\string\\\noexpand\hline}
\typeout{AI:\actprefix\arabic{aacti},#1,#2,#3}%
}

% the actual oldaction macro
\def\p@aact#1{\csname actprefix\endcsname}
\providecommand{\oldaction}[4]{
\protected@edef\@currentlabel{\csname p@aact\endcsname-\theaacti}%
\ifthenelse{\boolean{@oldactstarted}}{\relax}{\immediate\openout8=oldactions\setboolean{@oldactstarted}{true}}
\immediate\write8{\noexpand\hypertarget{#1}{#1} & #2 & #3 & #4\string\\\noexpand\hline}
\marginlabel{AI \hyperlink{#1}{#1}}%
\typeout{AI:#1,#2,#3,#4}%
}

% Parameterized the widths of the action table in case tweaking is needed.
% DWE 3/12/08

\newcommand{\actionActionNumberWidth}{.11\textwidth}
\newcommand{\actionActioneeWidth}{.12\textwidth}
\newcommand{\actionActionDateWidth}{.12\textwidth}
\newcommand{\actionActionDescriptionWidth}{.56\textwidth}

% outputs the list of actions if any are defined
\providecommand{\listofactions}{%
\IfFileExists{actions}{%
\immediate\closeout7
\immediate\closeout8
\newcounter{actli}
\setcounter{actli}{1}
\newcommand{\countact}{\nplpadding{2}\numprint{\arabic{actli}}\addtocounter{actli}{1}}
\begin{longtable}{|p{\actionActionNumberWidth}|>{\raggedright}p{\actionActioneeWidth}|>
{\raggedright}p{\actionActionDateWidth}|p{\actionActionDescriptionWidth}|}
\hline
Id & Actionee & Due Date & Action\\\hline
\IfFileExists{oldactions}{\input{oldactions}}{}
\input{actions}
\end{longtable}
}{%
No actions have been identified.}
}

% -----------------------------------------------------------------------------
% Useful definition
% -----------------------------------------------------------------------------
\def\aap{A\&A}             % Astronomy and Astrophysics
\def\ssr{Space~Sci.~Rev.}  % Space Science Reviews
\def\apj{ApJ}              % Astrophysical Journal
\def\aj{AJ}                % Astronomical Journal
\def\mnras{MNRAS}          % Monthly Notices of the RAS
\def\araa{ARA\&A}          % Annual Review of Astron and Astrophys
\def\nat{Nature}           % Nature
\def\apjl{ApJ}             % Astrophysical Journal, Letters

\def\degr{\hbox{$^\circ$}} 
\def\arcmin{\hbox{$^\prime$}}
\def\arcsec{\hbox{$^{\prime\prime}$}}
\def\fs{\hbox{$.\!\!^{\rm s}$}}
\def\fdg{\hbox{$.\!\!^\circ$}}
\def\farcm{\hbox{$.\mkern-4mu^\prime$}}
\def\farcs{\hbox{$.\!\!^{\prime\prime}$}}
\def\sun{\hbox{$\odot$}}

%
% this makes list spacing single spaced.
%
\newenvironment{enumerate_single}{
\begin{enumerate}
  \setlength{\itemsep}{1pt}
  \setlength{\parskip}{0pt}
  \setlength{\parsep}{0pt}}
{\end{enumerate}
}
\newenvironment{itemize_single}{
\begin{itemize}
  \setlength{\itemsep}{1pt}
  \setlength{\parskip}{0pt}
  \setlength{\parsep}{0pt}}
{\end{itemize}
}

%
%   convenience macros
%
\providecommand{\pu}[2]{\ensuremath{#1\,\mbox{#2}}}
\providecommand{\secs}[1]{\pu{#1}{s}}
\providecommand{\uas}[1]{\pu{#1}{$\mu$as}}
\providecommand{\muas}[1]{\pu{#1}{$\mu$as}}
\providecommand{\muasonly}{\ensuremath{\mu\mbox{as}}}
\providecommand{\inp}[1]{{\tt #1}}
\providecommand{\prog}[1]{{\it #1}}
\providecommand{\secref}[1]{Sect.~\ref{#1}}
\providecommand{\appref}[1]{Apndx.~\ref{#1}}
\providecommand{\partref}[1]{Part~\ref{#1}}
\providecommand{\tabref}[1]{Tab.~\ref{#1}}
\providecommand{\figref}[1]{Fig.~\ref{#1}}
\providecommand{\eqnref}[1]{Eq.~\ref{#1}}
\providecommand{\reqref}[1]{Req.~\ref{#1}}
\providecommand{\actref}[1]{AI~\ref{#1}}
\providecommand{\class}[1]{{\it #1}}
\providecommand{\pack}[1]{{\em #1}}
\providecommand{\property}[1]{{\em #1}}
\providecommand{\method}[1]{{\em #1}}
\providecommand{\file}[1]{{\em #1}}
\providecommand{\directory}[1]{{\em #1}}
\providecommand{\code}[1]{{\tt #1}}

% new bib
\newcommand{\citell}{\citeyear}
\newcommand{\citellp}{\citeyearpar}

\renewcommand{\vec}[1]{\ensuremath{\mathchoice{\mbox{\boldmath$\displaystyle#1$}}
{\mbox{\boldmath$\textstyle#1$}}
{\mbox{\boldmath$\scriptstyle#1$}}
{\mbox{\boldmath$\scriptscriptstyle#1$}}}}

%------------------ caption format ----------------------------
% added by LL to get nicer captions to tables and figures
% makecaption redefined (small, FIGURE in sc, 0.9\hsize):
\setlength\abovecaptionskip{10\p@}
\setlength\belowcaptionskip{0\p@}
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{\small {\sc #1:} #2}%
  \ifdim \wd\@tempboxa >0.9\hsize
    \hb@xt@\hsize{\hfil\parbox{0.9\hsize}{\small {\sc #1:} #2}\hfil} %\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}
%------------------ end caption format ----------------------------

%----------------- Paragraph numbering - JSH

% put \npara at the start of each paragraph or \item you want to be numbered

\newcounter{@dfparincr}
\setcounter{@dfparincr}{5}

\newcounter{gaiapar}
\providecommand{\thegaiapar}{\numprint{\arabic{gaiapar}}}
\providecommand{\npara}{
\addtocounter{gaiapar}{\value{nparaincr}}
\marginlabel{\S\thegaiapar}}

% default increment for requirement counter
\providecommand{\setnparaincr}[1]{\setcounter{@dfparincr}{#1}}
\newcounter{nparaincr}
\setcounter{nparaincr}{\value{@dfparincr}}

%-----------------------