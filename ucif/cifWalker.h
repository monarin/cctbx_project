/** \file
 *  This C header file was generated by $ANTLR version 3.4
 *
 *     -  From the grammar source file : cifWalker.g
 *     -                            On : 2011-09-15 11:54:10
 *     -           for the tree parser : cifWalkerTreeParser
 *
 * Editing it, at least manually, is not wise.
 *
 * C language generator and runtime by Jim Idle, jimi|hereisanat|idle|dotgoeshere|ws.
 *
 *
 * The tree parser
cifWalker

has the callable functions (rules) shown below,
 * which will invoke the code for the associated rule in the source grammar
 * assuming that the input stream is pointing to a token/text stream that could begin
 * this rule.
 *
 * For instance if you call the first (topmost) rule in a parser grammar, you will
 * get the results of a full parse, but calling a rule half way through the grammar will
 * allow you to pass part of a full token stream to the parser, such as for syntax checking
 * in editors and so on.
 *
 * The parser entry points are called indirectly (by function pointer to function) via
 * a parser context typedef pcifWalker, which is returned from a call to cifWalkerNew().
 *
 * The methods in pcifWalker are  as follows:
 *
 *  -
 void
      pcifWalker->parse(pcifWalker)
 *  -
 void
      pcifWalker->cif(pcifWalker)
 *  -
 void
      pcifWalker->loop_body(pcifWalker)
 *  -
 void
      pcifWalker->save_frame(pcifWalker)
 *  -
 void
      pcifWalker->data_items(pcifWalker)
 *  -
 cifWalker_data_block_heading_return
      pcifWalker->data_block_heading(pcifWalker)
 *  -
 void
      pcifWalker->data_block(pcifWalker)
 *  -
 void
      pcifWalker->loop_header(pcifWalker)
 *  -
 void
      pcifWalker->inapplicable(pcifWalker)
 *  -
 void
      pcifWalker->unknown(pcifWalker)
 *  -
 cifWalker_value_return
      pcifWalker->value(pcifWalker)
 *  -
 void
      pcifWalker->char_string(pcifWalker)
 *  -
 void
      pcifWalker->text_field(pcifWalker)
 *
 * The return type for any particular rule is of course determined by the source
 * grammar file.
 */
// [The "BSD license"]
// Copyright (c) 2005-2009 Jim Idle, Temporal Wave LLC
// http://www.temporal-wave.com
// http://www.linkedin.com/in/jimidle
//
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
// 3. The name of the author may not be used to endorse or promote products
//    derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
// IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
// OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
// IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
// NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
// THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#ifndef _cifWalker_H
#define _cifWalker_H
/* =============================================================================
 * Standard antlr3 C runtime definitions
 */
#include    <antlr3.h>

/* End of standard antlr 3 runtime definitions
 * =============================================================================
 */

#include <string>
#include <ucif/builder.h>


#ifdef __cplusplus
extern "C" {
#endif

// Forward declare the context typedef so that we can use it before it is
// properly defined. Delegators and delegates (from import statements) are
// interdependent and their context structures contain pointers to each other
// C only allows such things to be declared if you pre-declare the typedef.
//
typedef struct cifWalker_Ctx_struct cifWalker, * pcifWalker;



#ifdef  ANTLR3_WINDOWS
// Disable: Unreferenced parameter,                                                     - Rules with parameters that are not used
//          constant conditional,                                                       - ANTLR realizes that a prediction is always true (synpred usually)
//          initialized but unused variable                                     - tree rewrite variables declared but not needed
//          Unreferenced local variable                                         - lexer rule declares but does not always use _type
//          potentially unitialized variable used                       - retval always returned from a rule
//                      unreferenced local function has been removed    - susually getTokenNames or freeScope, they can go without warnigns
//
// These are only really displayed at warning level /W4 but that is the code ideal I am aiming at
// and the codegen must generate some of these warnings by necessity, apart from 4100, which is
// usually generated when a parser rule is given a parameter that it does not use. Mostly though
// this is a matter of orthogonality hence I disable that one.
//
#pragma warning( disable : 4100 )
#pragma warning( disable : 4101 )
#pragma warning( disable : 4127 )
#pragma warning( disable : 4189 )
#pragma warning( disable : 4505 )
#pragma warning( disable : 4701 )
#endif
typedef struct cifWalker_data_block_heading_return_struct
{
    pANTLR3_BASE_TREE       start;
    pANTLR3_BASE_TREE       stop;
}
    cifWalker_data_block_heading_return;



typedef struct cifWalker_value_return_struct
{
    pANTLR3_BASE_TREE       start;
    pANTLR3_BASE_TREE       stop;
}
    cifWalker_value_return;





/* ruleAttributeScopeDecl(scope)
 */
/* makeScopeSet()
 */
 /** Definition of the parse scope variable tracking
 *  structure. An instance of this structure is created by calling
 *  cifWalker_parsePush().
 */
typedef struct  cifWalker_parse_SCOPE_struct
{
    /** Function that the user may provide to be called when the
     *  scope is destroyed (so you can free pANTLR3_HASH_TABLES and so on)
     *
     * \param POinter to an instance of this typedef/struct
     */
    void    (ANTLR3_CDECL *free)        (struct cifWalker_parse_SCOPE_struct * frame);

    /* =============================================================================
     * Programmer defined variables...
     */
    ucif::builder_base* builder;

    /* End of programmer defined variables
     * =============================================================================
     */
}
    cifWalker_parse_SCOPE, * pcifWalker_parse_SCOPE;


/* ruleAttributeScopeDecl(scope)
 */
/* makeScopeSet()
 */
 /** Definition of the data_items scope variable tracking
 *  structure. An instance of this structure is created by calling
 *  cifWalker_data_itemsPush().
 */
typedef struct  cifWalker_data_items_SCOPE_struct
{
    /** Function that the user may provide to be called when the
     *  scope is destroyed (so you can free pANTLR3_HASH_TABLES and so on)
     *
     * \param POinter to an instance of this typedef/struct
     */
    void    (ANTLR3_CDECL *free)        (struct cifWalker_data_items_SCOPE_struct * frame);

    /* =============================================================================
     * Programmer defined variables...
     */
    ucif::array_wrapper_base* curr_loop_values;
    ucif::array_wrapper_base* curr_loop_headers;

    /* End of programmer defined variables
     * =============================================================================
     */
}
    cifWalker_data_items_SCOPE, * pcifWalker_data_items_SCOPE;


/** Context tracking structure for
cifWalker

 */
struct cifWalker_Ctx_struct
{
    /** Built in ANTLR3 context tracker contains all the generic elements
     *  required for context tracking.
     */
    pANTLR3_TREE_PARSER     pTreeParser;

    /* ruleAttributeScopeDef(scope)
     */
    /** Pointer to the  parse stack for use by pcifWalker_parsePush()
     *  and pcifWalker_parsePop()
     */
    pANTLR3_STACK pcifWalker_parseStack;
    ANTLR3_UINT32 pcifWalker_parseStack_limit;
    pcifWalker_parse_SCOPE   (*pcifWalker_parsePush)(struct cifWalker_Ctx_struct * ctx);
    pcifWalker_parse_SCOPE   pcifWalker_parseTop;


    /* ruleAttributeScopeDef(scope)
     */
    /** Pointer to the  data_items stack for use by pcifWalker_data_itemsPush()
     *  and pcifWalker_data_itemsPop()
     */
    pANTLR3_STACK pcifWalker_data_itemsStack;
    ANTLR3_UINT32 pcifWalker_data_itemsStack_limit;
    pcifWalker_data_items_SCOPE   (*pcifWalker_data_itemsPush)(struct cifWalker_Ctx_struct * ctx);
    pcifWalker_data_items_SCOPE   pcifWalker_data_itemsTop;




     void
     (*parse)   (struct cifWalker_Ctx_struct * ctx, ucif::builder_base* builder_);

     void
     (*cif)     (struct cifWalker_Ctx_struct * ctx);

     void
     (*loop_body)       (struct cifWalker_Ctx_struct * ctx);

     void
     (*save_frame)      (struct cifWalker_Ctx_struct * ctx);

     void
     (*data_items)      (struct cifWalker_Ctx_struct * ctx);

     cifWalker_data_block_heading_return
     (*data_block_heading)      (struct cifWalker_Ctx_struct * ctx);

     void
     (*data_block)      (struct cifWalker_Ctx_struct * ctx);

     void
     (*loop_header)     (struct cifWalker_Ctx_struct * ctx);

     void
     (*inapplicable)    (struct cifWalker_Ctx_struct * ctx);

     void
     (*unknown) (struct cifWalker_Ctx_struct * ctx);

     cifWalker_value_return
     (*value)   (struct cifWalker_Ctx_struct * ctx);

     void
     (*char_string)     (struct cifWalker_Ctx_struct * ctx);

     void
     (*text_field)      (struct cifWalker_Ctx_struct * ctx);
    // Delegated rules

    const char * (*getGrammarFileName)();
    void            (*reset)  (struct cifWalker_Ctx_struct * ctx);
    void            (*free)   (struct cifWalker_Ctx_struct * ctx);

      ucif::array_wrapper_base* errors;

};

// Function protoypes for the constructor functions that external translation units
// such as delegators and delegates may wish to call.
//
ANTLR3_API pcifWalker cifWalkerNew         (
pANTLR3_COMMON_TREE_NODE_STREAM
 instream);
ANTLR3_API pcifWalker cifWalkerNewSSD      (
pANTLR3_COMMON_TREE_NODE_STREAM
 instream, pANTLR3_RECOGNIZER_SHARED_STATE state);

/** Symbolic definitions of all the tokens that the
tree parser
 will work with.
 * \{
 *
 * Antlr will define EOF, but we can't use that as it it is too common in
 * in C header files and that would be confusing. There is no way to filter this out at the moment
 * so we just undef it here for now. That isn't the value we get back from C recognizers
 * anyway. We are looking for ANTLR3_TOKEN_EOF.
 */
#ifdef  EOF
#undef  EOF
#endif
#ifdef  Tokens
#undef  Tokens
#endif
#define EOF      -1
#define T__41      41
#define ANY_PRINT_CHAR      4
#define CHAR_STRING      5
#define CIF      6
#define COMMENTS      7
#define DATA_      8
#define DATA_BLOCK      9
#define DATA_BLOCK_HEADING      10
#define DIGIT      11
#define DOUBLE_QUOTE      12
#define DOUBLE_QUOTED_STRING      13
#define EOL      14
#define EXPONENT      15
#define FLOAT      16
#define GLOBAL_      17
#define INAPPLICABLE      18
#define INTEGER      19
#define LOOP      20
#define LOOP_      21
#define NON_BLANK_CHAR      22
#define NON_BLANK_CHAR_      23
#define NUMBER      24
#define NUMERIC      25
#define ORDINARY_CHAR      26
#define SAVE      27
#define SAVE_      28
#define SAVE_FRAME_HEADING      29
#define SEMI_COLON_TEXT_FIELD      30
#define SINGLE_QUOTE      31
#define SINGLE_QUOTED_STRING      32
#define STOP_      33
#define TAG      34
#define TAG_VALUE_PAIR      35
#define TEXT_LEAD_CHAR      36
#define UNKNOWN      37
#define UNQUOTED_STRING      38
#define UNSIGNED_INTEGER      39
#define WHITESPACE      40
#define T__42      42
#define T__43      43
#ifdef  EOF
#undef  EOF
#define EOF     ANTLR3_TOKEN_EOF
#endif

#ifndef TOKENSOURCE
#define TOKENSOURCE(lxr) lxr->pLexer->rec->state->tokSource
#endif

/* End of token definitions for cifWalker
 * =============================================================================
 */
/** } */

#ifdef __cplusplus
}
#endif

#endif

/* END - Note:Keep extra line feed to satisfy UNIX systems */
