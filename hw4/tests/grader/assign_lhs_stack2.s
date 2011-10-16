.globl main
main:
	push %ebp
	movl %esp,%ebp
	subl $416,%esp
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1
	call inject_int
	jmp label2
	label1:
	cmpl $1,%eax
	jne label3
	call inject_bool
	jmp label4
	label3:
	cmpl $3,%eax
	jne label5
	call inject_big
	jmp label6
	label5:
	label6:
	label4:
	label2:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-312(%ebp)
	call input
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label7
	call inject_int
	jmp label8
	label7:
	cmpl $1,%eax
	jne label9
	call inject_bool
	jmp label10
	label9:
	cmpl $3,%eax
	jne label11
	call inject_big
	jmp label12
	label11:
	label12:
	label10:
	label8:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-372(%ebp)
	movl -312(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label13
	call inject_int
	jmp label14
	label13:
	cmpl $1,%eax
	jne label15
	call inject_bool
	jmp label16
	label15:
	cmpl $3,%eax
	jne label17
	call inject_big
	jmp label18
	label17:
	label18:
	label16:
	label14:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label19
	call inject_int
	jmp label20
	label19:
	cmpl $1,%eax
	jne label21
	call inject_bool
	jmp label22
	label21:
	cmpl $3,%eax
	jne label23
	call inject_big
	jmp label24
	label23:
	label24:
	label22:
	label20:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label25
	movl $1,-8(%ebp)
	jmp label26
	label25:
	movl $0,-8(%ebp)
	label26:
	movl -8(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label27
	call inject_int
	jmp label28
	label27:
	cmpl $1,%eax
	jne label29
	call inject_bool
	jmp label30
	label29:
	cmpl $3,%eax
	jne label31
	call inject_big
	jmp label32
	label31:
	label32:
	label30:
	label28:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label33
	call inject_int
	jmp label34
	label33:
	cmpl $1,%eax
	jne label35
	call inject_bool
	jmp label36
	label35:
	cmpl $3,%eax
	jne label37
	call inject_big
	jmp label38
	label37:
	label38:
	label36:
	label34:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label39
	call inject_int
	jmp label40
	label39:
	cmpl $1,%eax
	jne label41
	call inject_bool
	jmp label42
	label41:
	cmpl $3,%eax
	jne label43
	call inject_big
	jmp label44
	label43:
	label44:
	label42:
	label40:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label45
	movl $1,-136(%ebp)
	jmp label46
	label45:
	movl $0,-136(%ebp)
	label46:
	movl -136(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label47
	call inject_int
	jmp label48
	label47:
	cmpl $1,%eax
	jne label49
	call inject_bool
	jmp label50
	label49:
	cmpl $3,%eax
	jne label51
	call inject_big
	jmp label52
	label51:
	label52:
	label50:
	label48:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label53
	movl -4(%ebp),%eax
	movl %eax,-132(%ebp)
	jmp label54
	label53:
	movl %ebx,%eax
	movl %eax,-132(%ebp)
	label54:
	addl $4,%esp
	movl -132(%ebp),%eax
	movl %eax,-132(%ebp)
	movl -132(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label55
	addl $4,%esp
	movl -312(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label57
	call project_int
	jmp label58
	label57:
	cmpl $1,%eax
	jne label59
	call project_bool
	jmp label60
	label59:
	cmpl $3,%eax
	jne label61
	call project_big
	jmp label62
	label61:
	label62:
	label60:
	label58:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label63
	call project_int
	jmp label64
	label63:
	cmpl $1,%eax
	jne label65
	call project_bool
	jmp label66
	label65:
	cmpl $3,%eax
	jne label67
	call project_big
	jmp label68
	label67:
	label68:
	label66:
	label64:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label69
	call inject_int
	jmp label70
	label69:
	cmpl $1,%eax
	jne label71
	call inject_bool
	jmp label72
	label71:
	cmpl $3,%eax
	jne label73
	call inject_big
	jmp label74
	label73:
	label74:
	label72:
	label70:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-28(%ebp)
	jmp label56
	label55:
	movl -312(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label75
	call inject_int
	jmp label76
	label75:
	cmpl $1,%eax
	jne label77
	call inject_bool
	jmp label78
	label77:
	cmpl $3,%eax
	jne label79
	call inject_big
	jmp label80
	label79:
	label80:
	label78:
	label76:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label81
	call inject_int
	jmp label82
	label81:
	cmpl $1,%eax
	jne label83
	call inject_bool
	jmp label84
	label83:
	cmpl $3,%eax
	jne label85
	call inject_big
	jmp label86
	label85:
	label86:
	label84:
	label82:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label87
	movl $1,-108(%ebp)
	jmp label88
	label87:
	movl $0,-108(%ebp)
	label88:
	movl -108(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label89
	call inject_int
	jmp label90
	label89:
	cmpl $1,%eax
	jne label91
	call inject_bool
	jmp label92
	label91:
	cmpl $3,%eax
	jne label93
	call inject_big
	jmp label94
	label93:
	label94:
	label92:
	label90:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label95
	call inject_int
	jmp label96
	label95:
	cmpl $1,%eax
	jne label97
	call inject_bool
	jmp label98
	label97:
	cmpl $3,%eax
	jne label99
	call inject_big
	jmp label100
	label99:
	label100:
	label98:
	label96:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label101
	call inject_int
	jmp label102
	label101:
	cmpl $1,%eax
	jne label103
	call inject_bool
	jmp label104
	label103:
	cmpl $3,%eax
	jne label105
	call inject_big
	jmp label106
	label105:
	label106:
	label104:
	label102:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label107
	movl $1,-284(%ebp)
	jmp label108
	label107:
	movl $0,-284(%ebp)
	label108:
	movl -284(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label109
	call inject_int
	jmp label110
	label109:
	cmpl $1,%eax
	jne label111
	call inject_bool
	jmp label112
	label111:
	cmpl $3,%eax
	jne label113
	call inject_big
	jmp label114
	label113:
	label114:
	label112:
	label110:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label115
	movl -4(%ebp),%eax
	movl %eax,-196(%ebp)
	jmp label116
	label115:
	movl %ebx,%eax
	movl %eax,-196(%ebp)
	label116:
	addl $4,%esp
	movl -196(%ebp),%eax
	movl %eax,-108(%ebp)
	movl -108(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label117
	addl $4,%esp
	movl -312(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label119
	call project_int
	jmp label120
	label119:
	cmpl $1,%eax
	jne label121
	call project_bool
	jmp label122
	label121:
	cmpl $3,%eax
	jne label123
	call project_big
	jmp label124
	label123:
	label124:
	label122:
	label120:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label125
	call project_int
	jmp label126
	label125:
	cmpl $1,%eax
	jne label127
	call project_bool
	jmp label128
	label127:
	cmpl $3,%eax
	jne label129
	call project_big
	jmp label130
	label129:
	label130:
	label128:
	label126:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label131
	call inject_int
	jmp label132
	label131:
	cmpl $1,%eax
	jne label133
	call inject_bool
	jmp label134
	label133:
	cmpl $3,%eax
	jne label135
	call inject_big
	jmp label136
	label135:
	label136:
	label134:
	label132:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-96(%ebp)
	jmp label118
	label117:
	movl -312(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label137
	call inject_int
	jmp label138
	label137:
	cmpl $1,%eax
	jne label139
	call inject_bool
	jmp label140
	label139:
	cmpl $3,%eax
	jne label141
	call inject_big
	jmp label142
	label141:
	label142:
	label140:
	label138:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label143
	call inject_int
	jmp label144
	label143:
	cmpl $1,%eax
	jne label145
	call inject_bool
	jmp label146
	label145:
	cmpl $3,%eax
	jne label147
	call inject_big
	jmp label148
	label147:
	label148:
	label146:
	label144:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label149
	movl $1,-16(%ebp)
	jmp label150
	label149:
	movl $0,-16(%ebp)
	label150:
	movl -16(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label151
	call inject_int
	jmp label152
	label151:
	cmpl $1,%eax
	jne label153
	call inject_bool
	jmp label154
	label153:
	cmpl $3,%eax
	jne label155
	call inject_big
	jmp label156
	label155:
	label156:
	label154:
	label152:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label157
	call inject_int
	jmp label158
	label157:
	cmpl $1,%eax
	jne label159
	call inject_bool
	jmp label160
	label159:
	cmpl $3,%eax
	jne label161
	call inject_big
	jmp label162
	label161:
	label162:
	label160:
	label158:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label163
	call inject_int
	jmp label164
	label163:
	cmpl $1,%eax
	jne label165
	call inject_bool
	jmp label166
	label165:
	cmpl $3,%eax
	jne label167
	call inject_big
	jmp label168
	label167:
	label168:
	label166:
	label164:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label169
	movl $1,-276(%ebp)
	jmp label170
	label169:
	movl $0,-276(%ebp)
	label170:
	movl -276(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label171
	call inject_int
	jmp label172
	label171:
	cmpl $1,%eax
	jne label173
	call inject_bool
	jmp label174
	label173:
	cmpl $3,%eax
	jne label175
	call inject_big
	jmp label176
	label175:
	label176:
	label174:
	label172:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label177
	movl -4(%ebp),%eax
	movl %eax,-12(%ebp)
	jmp label178
	label177:
	movl %ebx,%eax
	movl %eax,-12(%ebp)
	label178:
	addl $4,%esp
	movl -12(%ebp),%eax
	movl %eax,-12(%ebp)
	movl -12(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label179
	addl $4,%esp
	movl -312(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label181
	call project_int
	jmp label182
	label181:
	cmpl $1,%eax
	jne label183
	call project_bool
	jmp label184
	label183:
	cmpl $3,%eax
	jne label185
	call project_big
	jmp label186
	label185:
	label186:
	label184:
	label182:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label187
	call project_int
	jmp label188
	label187:
	cmpl $1,%eax
	jne label189
	call project_bool
	jmp label190
	label189:
	cmpl $3,%eax
	jne label191
	call project_big
	jmp label192
	label191:
	label192:
	label190:
	label188:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label193
	call inject_int
	jmp label194
	label193:
	cmpl $1,%eax
	jne label195
	call inject_bool
	jmp label196
	label195:
	cmpl $3,%eax
	jne label197
	call inject_big
	jmp label198
	label197:
	label198:
	label196:
	label194:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-404(%ebp)
	jmp label180
	label179:
	movl -312(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label199
	call inject_int
	jmp label200
	label199:
	cmpl $1,%eax
	jne label201
	call inject_bool
	jmp label202
	label201:
	cmpl $3,%eax
	jne label203
	call inject_big
	jmp label204
	label203:
	label204:
	label202:
	label200:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label205
	call inject_int
	jmp label206
	label205:
	cmpl $1,%eax
	jne label207
	call inject_bool
	jmp label208
	label207:
	cmpl $3,%eax
	jne label209
	call inject_big
	jmp label210
	label209:
	label210:
	label208:
	label206:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label211
	movl $1,-264(%ebp)
	jmp label212
	label211:
	movl $0,-264(%ebp)
	label212:
	movl -264(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label213
	call inject_int
	jmp label214
	label213:
	cmpl $1,%eax
	jne label215
	call inject_bool
	jmp label216
	label215:
	cmpl $3,%eax
	jne label217
	call inject_big
	jmp label218
	label217:
	label218:
	label216:
	label214:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label219
	call inject_int
	jmp label220
	label219:
	cmpl $1,%eax
	jne label221
	call inject_bool
	jmp label222
	label221:
	cmpl $3,%eax
	jne label223
	call inject_big
	jmp label224
	label223:
	label224:
	label222:
	label220:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label225
	call inject_int
	jmp label226
	label225:
	cmpl $1,%eax
	jne label227
	call inject_bool
	jmp label228
	label227:
	cmpl $3,%eax
	jne label229
	call inject_big
	jmp label230
	label229:
	label230:
	label228:
	label226:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label231
	movl $1,-92(%ebp)
	jmp label232
	label231:
	movl $0,-92(%ebp)
	label232:
	movl -92(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label233
	call inject_int
	jmp label234
	label233:
	cmpl $1,%eax
	jne label235
	call inject_bool
	jmp label236
	label235:
	cmpl $3,%eax
	jne label237
	call inject_big
	jmp label238
	label237:
	label238:
	label236:
	label234:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label239
	movl -4(%ebp),%eax
	movl %eax,-112(%ebp)
	jmp label240
	label239:
	movl %ebx,%eax
	movl %eax,-112(%ebp)
	label240:
	addl $4,%esp
	movl -112(%ebp),%eax
	movl %eax,-8(%ebp)
	movl -8(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label241
	addl $4,%esp
	movl -312(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label243
	call project_int
	jmp label244
	label243:
	cmpl $1,%eax
	jne label245
	call project_bool
	jmp label246
	label245:
	cmpl $3,%eax
	jne label247
	call project_big
	jmp label248
	label247:
	label248:
	label246:
	label244:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label249
	call project_int
	jmp label250
	label249:
	cmpl $1,%eax
	jne label251
	call project_bool
	jmp label252
	label251:
	cmpl $3,%eax
	jne label253
	call project_big
	jmp label254
	label253:
	label254:
	label252:
	label250:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label255
	call inject_int
	jmp label256
	label255:
	cmpl $1,%eax
	jne label257
	call inject_bool
	jmp label258
	label257:
	cmpl $3,%eax
	jne label259
	call inject_big
	jmp label260
	label259:
	label260:
	label258:
	label256:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-24(%ebp)
	jmp label242
	label241:
	movl -312(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label261
	call inject_int
	jmp label262
	label261:
	cmpl $1,%eax
	jne label263
	call inject_bool
	jmp label264
	label263:
	cmpl $3,%eax
	jne label265
	call inject_big
	jmp label266
	label265:
	label266:
	label264:
	label262:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label267
	call inject_int
	jmp label268
	label267:
	cmpl $1,%eax
	jne label269
	call inject_bool
	jmp label270
	label269:
	cmpl $3,%eax
	jne label271
	call inject_big
	jmp label272
	label271:
	label272:
	label270:
	label268:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label273
	movl $1,-20(%ebp)
	jmp label274
	label273:
	movl $0,-20(%ebp)
	label274:
	movl -20(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label275
	call inject_int
	jmp label276
	label275:
	cmpl $1,%eax
	jne label277
	call inject_bool
	jmp label278
	label277:
	cmpl $3,%eax
	jne label279
	call inject_big
	jmp label280
	label279:
	label280:
	label278:
	label276:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -372(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label281
	call inject_int
	jmp label282
	label281:
	cmpl $1,%eax
	jne label283
	call inject_bool
	jmp label284
	label283:
	cmpl $3,%eax
	jne label285
	call inject_big
	jmp label286
	label285:
	label286:
	label284:
	label282:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label287
	call inject_int
	jmp label288
	label287:
	cmpl $1,%eax
	jne label289
	call inject_bool
	jmp label290
	label289:
	cmpl $3,%eax
	jne label291
	call inject_big
	jmp label292
	label291:
	label292:
	label290:
	label288:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label293
	movl $1,-32(%ebp)
	jmp label294
	label293:
	movl $0,-32(%ebp)
	label294:
	movl -32(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label295
	call inject_int
	jmp label296
	label295:
	cmpl $1,%eax
	jne label297
	call inject_bool
	jmp label298
	label297:
	cmpl $3,%eax
	jne label299
	call inject_big
	jmp label300
	label299:
	label300:
	label298:
	label296:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label301
	movl -4(%ebp),%eax
	movl %eax,-364(%ebp)
	jmp label302
	label301:
	movl %ebx,%eax
	movl %eax,-364(%ebp)
	label302:
	addl $4,%esp
	movl -364(%ebp),%eax
	movl %eax,-4(%ebp)
	movl -4(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label303
	addl $4,%esp
	movl -312(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label305
	call project_int
	jmp label306
	label305:
	cmpl $1,%eax
	jne label307
	call project_bool
	jmp label308
	label307:
	cmpl $3,%eax
	jne label309
	call project_big
	jmp label310
	label309:
	label310:
	label308:
	label306:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -372(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label311
	call project_int
	jmp label312
	label311:
	cmpl $1,%eax
	jne label313
	call project_bool
	jmp label314
	label313:
	cmpl $3,%eax
	jne label315
	call project_big
	jmp label316
	label315:
	label316:
	label314:
	label312:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	pushl %eax
	pushl %ebx
	call add
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label317
	call inject_int
	jmp label318
	label317:
	cmpl $1,%eax
	jne label319
	call inject_bool
	jmp label320
	label319:
	cmpl $3,%eax
	jne label321
	call inject_big
	jmp label322
	label321:
	label322:
	label320:
	label318:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-332(%ebp)
	jmp label304
	label303:
	call type_error
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-332(%ebp)
	label304:
	movl -332(%ebp),%eax
	movl %eax,-24(%ebp)
	label242:
	movl -24(%ebp),%eax
	movl %eax,-404(%ebp)
	label180:
	movl -404(%ebp),%eax
	movl %eax,-96(%ebp)
	label118:
	movl -96(%ebp),%eax
	movl %eax,-28(%ebp)
	label56:
	movl -28(%ebp),%eax
	movl %eax,-92(%ebp)
	movl -92(%ebp),%eax
	movl %eax,-28(%ebp)
	movl -92(%ebp),%eax
	movl %eax,-32(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label323
	call inject_int
	jmp label324
	label323:
	cmpl $1,%eax
	jne label325
	call inject_bool
	jmp label326
	label325:
	cmpl $3,%eax
	jne label327
	call inject_big
	jmp label328
	label327:
	label328:
	label326:
	label324:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label329
	call inject_int
	jmp label330
	label329:
	cmpl $1,%eax
	jne label331
	call inject_bool
	jmp label332
	label331:
	cmpl $3,%eax
	jne label333
	call inject_big
	jmp label334
	label333:
	label334:
	label332:
	label330:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label335
	movl $1,-224(%ebp)
	jmp label336
	label335:
	movl $0,-224(%ebp)
	label336:
	movl -224(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label337
	call inject_int
	jmp label338
	label337:
	cmpl $1,%eax
	jne label339
	call inject_bool
	jmp label340
	label339:
	cmpl $3,%eax
	jne label341
	call inject_big
	jmp label342
	label341:
	label342:
	label340:
	label338:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label343
	call inject_int
	jmp label344
	label343:
	cmpl $1,%eax
	jne label345
	call inject_bool
	jmp label346
	label345:
	cmpl $3,%eax
	jne label347
	call inject_big
	jmp label348
	label347:
	label348:
	label346:
	label344:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label349
	call inject_int
	jmp label350
	label349:
	cmpl $1,%eax
	jne label351
	call inject_bool
	jmp label352
	label351:
	cmpl $3,%eax
	jne label353
	call inject_big
	jmp label354
	label353:
	label354:
	label352:
	label350:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label355
	movl $1,-412(%ebp)
	jmp label356
	label355:
	movl $0,-412(%ebp)
	label356:
	movl -412(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label357
	call inject_int
	jmp label358
	label357:
	cmpl $1,%eax
	jne label359
	call inject_bool
	jmp label360
	label359:
	cmpl $3,%eax
	jne label361
	call inject_big
	jmp label362
	label361:
	label362:
	label360:
	label358:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label363
	movl -4(%ebp),%eax
	movl %eax,-348(%ebp)
	jmp label364
	label363:
	movl %ebx,%eax
	movl %eax,-348(%ebp)
	label364:
	addl $4,%esp
	movl -348(%ebp),%eax
	movl %eax,-24(%ebp)
	movl -24(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label365
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label367
	call project_int
	jmp label368
	label367:
	cmpl $1,%eax
	jne label369
	call project_bool
	jmp label370
	label369:
	cmpl $3,%eax
	jne label371
	call project_big
	jmp label372
	label371:
	label372:
	label370:
	label368:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label373
	call project_int
	jmp label374
	label373:
	cmpl $1,%eax
	jne label375
	call project_bool
	jmp label376
	label375:
	cmpl $3,%eax
	jne label377
	call project_big
	jmp label378
	label377:
	label378:
	label376:
	label374:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label379
	call inject_int
	jmp label380
	label379:
	cmpl $1,%eax
	jne label381
	call inject_bool
	jmp label382
	label381:
	cmpl $3,%eax
	jne label383
	call inject_big
	jmp label384
	label383:
	label384:
	label382:
	label380:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-36(%ebp)
	jmp label366
	label365:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label385
	call inject_int
	jmp label386
	label385:
	cmpl $1,%eax
	jne label387
	call inject_bool
	jmp label388
	label387:
	cmpl $3,%eax
	jne label389
	call inject_big
	jmp label390
	label389:
	label390:
	label388:
	label386:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label391
	call inject_int
	jmp label392
	label391:
	cmpl $1,%eax
	jne label393
	call inject_bool
	jmp label394
	label393:
	cmpl $3,%eax
	jne label395
	call inject_big
	jmp label396
	label395:
	label396:
	label394:
	label392:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label397
	movl $1,-148(%ebp)
	jmp label398
	label397:
	movl $0,-148(%ebp)
	label398:
	movl -148(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label399
	call inject_int
	jmp label400
	label399:
	cmpl $1,%eax
	jne label401
	call inject_bool
	jmp label402
	label401:
	cmpl $3,%eax
	jne label403
	call inject_big
	jmp label404
	label403:
	label404:
	label402:
	label400:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label405
	call inject_int
	jmp label406
	label405:
	cmpl $1,%eax
	jne label407
	call inject_bool
	jmp label408
	label407:
	cmpl $3,%eax
	jne label409
	call inject_big
	jmp label410
	label409:
	label410:
	label408:
	label406:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label411
	call inject_int
	jmp label412
	label411:
	cmpl $1,%eax
	jne label413
	call inject_bool
	jmp label414
	label413:
	cmpl $3,%eax
	jne label415
	call inject_big
	jmp label416
	label415:
	label416:
	label414:
	label412:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label417
	movl $1,-384(%ebp)
	jmp label418
	label417:
	movl $0,-384(%ebp)
	label418:
	movl -384(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label419
	call inject_int
	jmp label420
	label419:
	cmpl $1,%eax
	jne label421
	call inject_bool
	jmp label422
	label421:
	cmpl $3,%eax
	jne label423
	call inject_big
	jmp label424
	label423:
	label424:
	label422:
	label420:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label425
	movl -4(%ebp),%eax
	movl %eax,-408(%ebp)
	jmp label426
	label425:
	movl %ebx,%eax
	movl %eax,-408(%ebp)
	label426:
	addl $4,%esp
	movl -408(%ebp),%eax
	movl %eax,-20(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label427
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label429
	call project_int
	jmp label430
	label429:
	cmpl $1,%eax
	jne label431
	call project_bool
	jmp label432
	label431:
	cmpl $3,%eax
	jne label433
	call project_big
	jmp label434
	label433:
	label434:
	label432:
	label430:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label435
	call project_int
	jmp label436
	label435:
	cmpl $1,%eax
	jne label437
	call project_bool
	jmp label438
	label437:
	cmpl $3,%eax
	jne label439
	call project_big
	jmp label440
	label439:
	label440:
	label438:
	label436:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label441
	call inject_int
	jmp label442
	label441:
	cmpl $1,%eax
	jne label443
	call inject_bool
	jmp label444
	label443:
	cmpl $3,%eax
	jne label445
	call inject_big
	jmp label446
	label445:
	label446:
	label444:
	label442:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-156(%ebp)
	jmp label428
	label427:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label447
	call inject_int
	jmp label448
	label447:
	cmpl $1,%eax
	jne label449
	call inject_bool
	jmp label450
	label449:
	cmpl $3,%eax
	jne label451
	call inject_big
	jmp label452
	label451:
	label452:
	label450:
	label448:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label453
	call inject_int
	jmp label454
	label453:
	cmpl $1,%eax
	jne label455
	call inject_bool
	jmp label456
	label455:
	cmpl $3,%eax
	jne label457
	call inject_big
	jmp label458
	label457:
	label458:
	label456:
	label454:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label459
	movl $1,-392(%ebp)
	jmp label460
	label459:
	movl $0,-392(%ebp)
	label460:
	movl -392(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label461
	call inject_int
	jmp label462
	label461:
	cmpl $1,%eax
	jne label463
	call inject_bool
	jmp label464
	label463:
	cmpl $3,%eax
	jne label465
	call inject_big
	jmp label466
	label465:
	label466:
	label464:
	label462:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label467
	call inject_int
	jmp label468
	label467:
	cmpl $1,%eax
	jne label469
	call inject_bool
	jmp label470
	label469:
	cmpl $3,%eax
	jne label471
	call inject_big
	jmp label472
	label471:
	label472:
	label470:
	label468:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label473
	call inject_int
	jmp label474
	label473:
	cmpl $1,%eax
	jne label475
	call inject_bool
	jmp label476
	label475:
	cmpl $3,%eax
	jne label477
	call inject_big
	jmp label478
	label477:
	label478:
	label476:
	label474:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label479
	movl $1,-272(%ebp)
	jmp label480
	label479:
	movl $0,-272(%ebp)
	label480:
	movl -272(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label481
	call inject_int
	jmp label482
	label481:
	cmpl $1,%eax
	jne label483
	call inject_bool
	jmp label484
	label483:
	cmpl $3,%eax
	jne label485
	call inject_big
	jmp label486
	label485:
	label486:
	label484:
	label482:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label487
	movl -4(%ebp),%eax
	movl %eax,-116(%ebp)
	jmp label488
	label487:
	movl %ebx,%eax
	movl %eax,-116(%ebp)
	label488:
	addl $4,%esp
	movl -116(%ebp),%eax
	movl %eax,-16(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label489
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label491
	call project_int
	jmp label492
	label491:
	cmpl $1,%eax
	jne label493
	call project_bool
	jmp label494
	label493:
	cmpl $3,%eax
	jne label495
	call project_big
	jmp label496
	label495:
	label496:
	label494:
	label492:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label497
	call project_int
	jmp label498
	label497:
	cmpl $1,%eax
	jne label499
	call project_bool
	jmp label500
	label499:
	cmpl $3,%eax
	jne label501
	call project_big
	jmp label502
	label501:
	label502:
	label500:
	label498:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label503
	call inject_int
	jmp label504
	label503:
	cmpl $1,%eax
	jne label505
	call inject_bool
	jmp label506
	label505:
	cmpl $3,%eax
	jne label507
	call inject_big
	jmp label508
	label507:
	label508:
	label506:
	label504:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-340(%ebp)
	jmp label490
	label489:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label509
	call inject_int
	jmp label510
	label509:
	cmpl $1,%eax
	jne label511
	call inject_bool
	jmp label512
	label511:
	cmpl $3,%eax
	jne label513
	call inject_big
	jmp label514
	label513:
	label514:
	label512:
	label510:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label515
	call inject_int
	jmp label516
	label515:
	cmpl $1,%eax
	jne label517
	call inject_bool
	jmp label518
	label517:
	cmpl $3,%eax
	jne label519
	call inject_big
	jmp label520
	label519:
	label520:
	label518:
	label516:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label521
	movl $1,-204(%ebp)
	jmp label522
	label521:
	movl $0,-204(%ebp)
	label522:
	movl -204(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label523
	call inject_int
	jmp label524
	label523:
	cmpl $1,%eax
	jne label525
	call inject_bool
	jmp label526
	label525:
	cmpl $3,%eax
	jne label527
	call inject_big
	jmp label528
	label527:
	label528:
	label526:
	label524:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label529
	call inject_int
	jmp label530
	label529:
	cmpl $1,%eax
	jne label531
	call inject_bool
	jmp label532
	label531:
	cmpl $3,%eax
	jne label533
	call inject_big
	jmp label534
	label533:
	label534:
	label532:
	label530:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label535
	call inject_int
	jmp label536
	label535:
	cmpl $1,%eax
	jne label537
	call inject_bool
	jmp label538
	label537:
	cmpl $3,%eax
	jne label539
	call inject_big
	jmp label540
	label539:
	label540:
	label538:
	label536:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label541
	movl $1,-88(%ebp)
	jmp label542
	label541:
	movl $0,-88(%ebp)
	label542:
	movl -88(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label543
	call inject_int
	jmp label544
	label543:
	cmpl $1,%eax
	jne label545
	call inject_bool
	jmp label546
	label545:
	cmpl $3,%eax
	jne label547
	call inject_big
	jmp label548
	label547:
	label548:
	label546:
	label544:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label549
	movl -4(%ebp),%eax
	movl %eax,-296(%ebp)
	jmp label550
	label549:
	movl %ebx,%eax
	movl %eax,-296(%ebp)
	label550:
	addl $4,%esp
	movl -296(%ebp),%eax
	movl %eax,-12(%ebp)
	movl -12(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label551
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label553
	call project_int
	jmp label554
	label553:
	cmpl $1,%eax
	jne label555
	call project_bool
	jmp label556
	label555:
	cmpl $3,%eax
	jne label557
	call project_big
	jmp label558
	label557:
	label558:
	label556:
	label554:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label559
	call project_int
	jmp label560
	label559:
	cmpl $1,%eax
	jne label561
	call project_bool
	jmp label562
	label561:
	cmpl $3,%eax
	jne label563
	call project_big
	jmp label564
	label563:
	label564:
	label562:
	label560:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label565
	call inject_int
	jmp label566
	label565:
	cmpl $1,%eax
	jne label567
	call inject_bool
	jmp label568
	label567:
	cmpl $3,%eax
	jne label569
	call inject_big
	jmp label570
	label569:
	label570:
	label568:
	label566:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-304(%ebp)
	jmp label552
	label551:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label571
	call inject_int
	jmp label572
	label571:
	cmpl $1,%eax
	jne label573
	call inject_bool
	jmp label574
	label573:
	cmpl $3,%eax
	jne label575
	call inject_big
	jmp label576
	label575:
	label576:
	label574:
	label572:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label577
	call inject_int
	jmp label578
	label577:
	cmpl $1,%eax
	jne label579
	call inject_bool
	jmp label580
	label579:
	cmpl $3,%eax
	jne label581
	call inject_big
	jmp label582
	label581:
	label582:
	label580:
	label578:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label583
	movl $1,-208(%ebp)
	jmp label584
	label583:
	movl $0,-208(%ebp)
	label584:
	movl -208(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label585
	call inject_int
	jmp label586
	label585:
	cmpl $1,%eax
	jne label587
	call inject_bool
	jmp label588
	label587:
	cmpl $3,%eax
	jne label589
	call inject_big
	jmp label590
	label589:
	label590:
	label588:
	label586:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label591
	call inject_int
	jmp label592
	label591:
	cmpl $1,%eax
	jne label593
	call inject_bool
	jmp label594
	label593:
	cmpl $3,%eax
	jne label595
	call inject_big
	jmp label596
	label595:
	label596:
	label594:
	label592:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label597
	call inject_int
	jmp label598
	label597:
	cmpl $1,%eax
	jne label599
	call inject_bool
	jmp label600
	label599:
	cmpl $3,%eax
	jne label601
	call inject_big
	jmp label602
	label601:
	label602:
	label600:
	label598:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label603
	movl $1,-100(%ebp)
	jmp label604
	label603:
	movl $0,-100(%ebp)
	label604:
	movl -100(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label605
	call inject_int
	jmp label606
	label605:
	cmpl $1,%eax
	jne label607
	call inject_bool
	jmp label608
	label607:
	cmpl $3,%eax
	jne label609
	call inject_big
	jmp label610
	label609:
	label610:
	label608:
	label606:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label611
	movl -4(%ebp),%eax
	movl %eax,-128(%ebp)
	jmp label612
	label611:
	movl %ebx,%eax
	movl %eax,-128(%ebp)
	label612:
	addl $4,%esp
	movl -128(%ebp),%eax
	movl %eax,-8(%ebp)
	movl -8(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label613
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label615
	call project_int
	jmp label616
	label615:
	cmpl $1,%eax
	jne label617
	call project_bool
	jmp label618
	label617:
	cmpl $3,%eax
	jne label619
	call project_big
	jmp label620
	label619:
	label620:
	label618:
	label616:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label621
	call project_int
	jmp label622
	label621:
	cmpl $1,%eax
	jne label623
	call project_bool
	jmp label624
	label623:
	cmpl $3,%eax
	jne label625
	call project_big
	jmp label626
	label625:
	label626:
	label624:
	label622:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	pushl %ebx
	pushl %eax
	call add
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label627
	call inject_int
	jmp label628
	label627:
	cmpl $1,%eax
	jne label629
	call inject_bool
	jmp label630
	label629:
	cmpl $3,%eax
	jne label631
	call inject_big
	jmp label632
	label631:
	label632:
	label630:
	label628:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-120(%ebp)
	jmp label614
	label613:
	call type_error
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-120(%ebp)
	label614:
	movl -120(%ebp),%eax
	movl %eax,-304(%ebp)
	label552:
	movl -304(%ebp),%eax
	movl %eax,-340(%ebp)
	label490:
	movl -340(%ebp),%eax
	movl %eax,-156(%ebp)
	label428:
	movl -156(%ebp),%eax
	movl %eax,-36(%ebp)
	label366:
	movl -36(%ebp),%eax
	movl %eax,-16(%ebp)
	movl -16(%ebp),%eax
	movl %eax,-12(%ebp)
	movl -16(%ebp),%eax
	movl %eax,-28(%ebp)
	movl -12(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label633
	call inject_int
	jmp label634
	label633:
	cmpl $1,%eax
	jne label635
	call inject_bool
	jmp label636
	label635:
	cmpl $3,%eax
	jne label637
	call inject_big
	jmp label638
	label637:
	label638:
	label636:
	label634:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label639
	call inject_int
	jmp label640
	label639:
	cmpl $1,%eax
	jne label641
	call inject_bool
	jmp label642
	label641:
	cmpl $3,%eax
	jne label643
	call inject_big
	jmp label644
	label643:
	label644:
	label642:
	label640:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label645
	movl $1,-80(%ebp)
	jmp label646
	label645:
	movl $0,-80(%ebp)
	label646:
	movl -80(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label647
	call inject_int
	jmp label648
	label647:
	cmpl $1,%eax
	jne label649
	call inject_bool
	jmp label650
	label649:
	cmpl $3,%eax
	jne label651
	call inject_big
	jmp label652
	label651:
	label652:
	label650:
	label648:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label653
	call inject_int
	jmp label654
	label653:
	cmpl $1,%eax
	jne label655
	call inject_bool
	jmp label656
	label655:
	cmpl $3,%eax
	jne label657
	call inject_big
	jmp label658
	label657:
	label658:
	label656:
	label654:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label659
	call inject_int
	jmp label660
	label659:
	cmpl $1,%eax
	jne label661
	call inject_bool
	jmp label662
	label661:
	cmpl $3,%eax
	jne label663
	call inject_big
	jmp label664
	label663:
	label664:
	label662:
	label660:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label665
	movl $1,-168(%ebp)
	jmp label666
	label665:
	movl $0,-168(%ebp)
	label666:
	movl -168(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label667
	call inject_int
	jmp label668
	label667:
	cmpl $1,%eax
	jne label669
	call inject_bool
	jmp label670
	label669:
	cmpl $3,%eax
	jne label671
	call inject_big
	jmp label672
	label671:
	label672:
	label670:
	label668:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label673
	movl -4(%ebp),%eax
	movl %eax,-184(%ebp)
	jmp label674
	label673:
	movl %ebx,%eax
	movl %eax,-184(%ebp)
	label674:
	addl $4,%esp
	movl -184(%ebp),%eax
	movl %eax,-32(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label675
	addl $4,%esp
	movl -12(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label677
	call project_int
	jmp label678
	label677:
	cmpl $1,%eax
	jne label679
	call project_bool
	jmp label680
	label679:
	cmpl $3,%eax
	jne label681
	call project_big
	jmp label682
	label681:
	label682:
	label680:
	label678:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label683
	call project_int
	jmp label684
	label683:
	cmpl $1,%eax
	jne label685
	call project_bool
	jmp label686
	label685:
	cmpl $3,%eax
	jne label687
	call project_big
	jmp label688
	label687:
	label688:
	label686:
	label684:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label689
	call inject_int
	jmp label690
	label689:
	cmpl $1,%eax
	jne label691
	call inject_bool
	jmp label692
	label691:
	cmpl $3,%eax
	jne label693
	call inject_big
	jmp label694
	label693:
	label694:
	label692:
	label690:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-240(%ebp)
	jmp label676
	label675:
	movl -12(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label695
	call inject_int
	jmp label696
	label695:
	cmpl $1,%eax
	jne label697
	call inject_bool
	jmp label698
	label697:
	cmpl $3,%eax
	jne label699
	call inject_big
	jmp label700
	label699:
	label700:
	label698:
	label696:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label701
	call inject_int
	jmp label702
	label701:
	cmpl $1,%eax
	jne label703
	call inject_bool
	jmp label704
	label703:
	cmpl $3,%eax
	jne label705
	call inject_big
	jmp label706
	label705:
	label706:
	label704:
	label702:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label707
	movl $1,-72(%ebp)
	jmp label708
	label707:
	movl $0,-72(%ebp)
	label708:
	movl -72(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label709
	call inject_int
	jmp label710
	label709:
	cmpl $1,%eax
	jne label711
	call inject_bool
	jmp label712
	label711:
	cmpl $3,%eax
	jne label713
	call inject_big
	jmp label714
	label713:
	label714:
	label712:
	label710:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label715
	call inject_int
	jmp label716
	label715:
	cmpl $1,%eax
	jne label717
	call inject_bool
	jmp label718
	label717:
	cmpl $3,%eax
	jne label719
	call inject_big
	jmp label720
	label719:
	label720:
	label718:
	label716:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label721
	call inject_int
	jmp label722
	label721:
	cmpl $1,%eax
	jne label723
	call inject_bool
	jmp label724
	label723:
	cmpl $3,%eax
	jne label725
	call inject_big
	jmp label726
	label725:
	label726:
	label724:
	label722:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label727
	movl $1,-320(%ebp)
	jmp label728
	label727:
	movl $0,-320(%ebp)
	label728:
	movl -320(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label729
	call inject_int
	jmp label730
	label729:
	cmpl $1,%eax
	jne label731
	call inject_bool
	jmp label732
	label731:
	cmpl $3,%eax
	jne label733
	call inject_big
	jmp label734
	label733:
	label734:
	label732:
	label730:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label735
	movl -4(%ebp),%eax
	movl %eax,-164(%ebp)
	jmp label736
	label735:
	movl %ebx,%eax
	movl %eax,-164(%ebp)
	label736:
	addl $4,%esp
	movl -164(%ebp),%eax
	movl %eax,-20(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label737
	addl $4,%esp
	movl -12(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label739
	call project_int
	jmp label740
	label739:
	cmpl $1,%eax
	jne label741
	call project_bool
	jmp label742
	label741:
	cmpl $3,%eax
	jne label743
	call project_big
	jmp label744
	label743:
	label744:
	label742:
	label740:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label745
	call project_int
	jmp label746
	label745:
	cmpl $1,%eax
	jne label747
	call project_bool
	jmp label748
	label747:
	cmpl $3,%eax
	jne label749
	call project_big
	jmp label750
	label749:
	label750:
	label748:
	label746:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label751
	call inject_int
	jmp label752
	label751:
	cmpl $1,%eax
	jne label753
	call inject_bool
	jmp label754
	label753:
	cmpl $3,%eax
	jne label755
	call inject_big
	jmp label756
	label755:
	label756:
	label754:
	label752:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-244(%ebp)
	jmp label738
	label737:
	movl -12(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label757
	call inject_int
	jmp label758
	label757:
	cmpl $1,%eax
	jne label759
	call inject_bool
	jmp label760
	label759:
	cmpl $3,%eax
	jne label761
	call inject_big
	jmp label762
	label761:
	label762:
	label760:
	label758:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label763
	call inject_int
	jmp label764
	label763:
	cmpl $1,%eax
	jne label765
	call inject_bool
	jmp label766
	label765:
	cmpl $3,%eax
	jne label767
	call inject_big
	jmp label768
	label767:
	label768:
	label766:
	label764:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label769
	movl $1,-124(%ebp)
	jmp label770
	label769:
	movl $0,-124(%ebp)
	label770:
	movl -124(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label771
	call inject_int
	jmp label772
	label771:
	cmpl $1,%eax
	jne label773
	call inject_bool
	jmp label774
	label773:
	cmpl $3,%eax
	jne label775
	call inject_big
	jmp label776
	label775:
	label776:
	label774:
	label772:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label777
	call inject_int
	jmp label778
	label777:
	cmpl $1,%eax
	jne label779
	call inject_bool
	jmp label780
	label779:
	cmpl $3,%eax
	jne label781
	call inject_big
	jmp label782
	label781:
	label782:
	label780:
	label778:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label783
	call inject_int
	jmp label784
	label783:
	cmpl $1,%eax
	jne label785
	call inject_bool
	jmp label786
	label785:
	cmpl $3,%eax
	jne label787
	call inject_big
	jmp label788
	label787:
	label788:
	label786:
	label784:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label789
	movl $1,-60(%ebp)
	jmp label790
	label789:
	movl $0,-60(%ebp)
	label790:
	movl -60(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label791
	call inject_int
	jmp label792
	label791:
	cmpl $1,%eax
	jne label793
	call inject_bool
	jmp label794
	label793:
	cmpl $3,%eax
	jne label795
	call inject_big
	jmp label796
	label795:
	label796:
	label794:
	label792:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label797
	movl -4(%ebp),%eax
	movl %eax,-40(%ebp)
	jmp label798
	label797:
	movl %ebx,%eax
	movl %eax,-40(%ebp)
	label798:
	addl $4,%esp
	movl -40(%ebp),%eax
	movl %eax,-24(%ebp)
	movl -24(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label799
	addl $4,%esp
	movl -12(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label801
	call project_int
	jmp label802
	label801:
	cmpl $1,%eax
	jne label803
	call project_bool
	jmp label804
	label803:
	cmpl $3,%eax
	jne label805
	call project_big
	jmp label806
	label805:
	label806:
	label804:
	label802:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label807
	call project_int
	jmp label808
	label807:
	cmpl $1,%eax
	jne label809
	call project_bool
	jmp label810
	label809:
	cmpl $3,%eax
	jne label811
	call project_big
	jmp label812
	label811:
	label812:
	label810:
	label808:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label813
	call inject_int
	jmp label814
	label813:
	cmpl $1,%eax
	jne label815
	call inject_bool
	jmp label816
	label815:
	cmpl $3,%eax
	jne label817
	call inject_big
	jmp label818
	label817:
	label818:
	label816:
	label814:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-76(%ebp)
	jmp label800
	label799:
	movl -12(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label819
	call inject_int
	jmp label820
	label819:
	cmpl $1,%eax
	jne label821
	call inject_bool
	jmp label822
	label821:
	cmpl $3,%eax
	jne label823
	call inject_big
	jmp label824
	label823:
	label824:
	label822:
	label820:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label825
	call inject_int
	jmp label826
	label825:
	cmpl $1,%eax
	jne label827
	call inject_bool
	jmp label828
	label827:
	cmpl $3,%eax
	jne label829
	call inject_big
	jmp label830
	label829:
	label830:
	label828:
	label826:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label831
	movl $1,-280(%ebp)
	jmp label832
	label831:
	movl $0,-280(%ebp)
	label832:
	movl -280(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label833
	call inject_int
	jmp label834
	label833:
	cmpl $1,%eax
	jne label835
	call inject_bool
	jmp label836
	label835:
	cmpl $3,%eax
	jne label837
	call inject_big
	jmp label838
	label837:
	label838:
	label836:
	label834:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label839
	call inject_int
	jmp label840
	label839:
	cmpl $1,%eax
	jne label841
	call inject_bool
	jmp label842
	label841:
	cmpl $3,%eax
	jne label843
	call inject_big
	jmp label844
	label843:
	label844:
	label842:
	label840:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label845
	call inject_int
	jmp label846
	label845:
	cmpl $1,%eax
	jne label847
	call inject_bool
	jmp label848
	label847:
	cmpl $3,%eax
	jne label849
	call inject_big
	jmp label850
	label849:
	label850:
	label848:
	label846:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label851
	movl $1,-352(%ebp)
	jmp label852
	label851:
	movl $0,-352(%ebp)
	label852:
	movl -352(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label853
	call inject_int
	jmp label854
	label853:
	cmpl $1,%eax
	jne label855
	call inject_bool
	jmp label856
	label855:
	cmpl $3,%eax
	jne label857
	call inject_big
	jmp label858
	label857:
	label858:
	label856:
	label854:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label859
	movl -4(%ebp),%eax
	movl %eax,-52(%ebp)
	jmp label860
	label859:
	movl %ebx,%eax
	movl %eax,-52(%ebp)
	label860:
	addl $4,%esp
	movl -52(%ebp),%eax
	movl %eax,-8(%ebp)
	movl -8(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label861
	addl $4,%esp
	movl -12(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label863
	call project_int
	jmp label864
	label863:
	cmpl $1,%eax
	jne label865
	call project_bool
	jmp label866
	label865:
	cmpl $3,%eax
	jne label867
	call project_big
	jmp label868
	label867:
	label868:
	label866:
	label864:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label869
	call project_int
	jmp label870
	label869:
	cmpl $1,%eax
	jne label871
	call project_bool
	jmp label872
	label871:
	cmpl $3,%eax
	jne label873
	call project_big
	jmp label874
	label873:
	label874:
	label872:
	label870:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label875
	call inject_int
	jmp label876
	label875:
	cmpl $1,%eax
	jne label877
	call inject_bool
	jmp label878
	label877:
	cmpl $3,%eax
	jne label879
	call inject_big
	jmp label880
	label879:
	label880:
	label878:
	label876:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-56(%ebp)
	jmp label862
	label861:
	movl -12(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label881
	call inject_int
	jmp label882
	label881:
	cmpl $1,%eax
	jne label883
	call inject_bool
	jmp label884
	label883:
	cmpl $3,%eax
	jne label885
	call inject_big
	jmp label886
	label885:
	label886:
	label884:
	label882:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label887
	call inject_int
	jmp label888
	label887:
	cmpl $1,%eax
	jne label889
	call inject_bool
	jmp label890
	label889:
	cmpl $3,%eax
	jne label891
	call inject_big
	jmp label892
	label891:
	label892:
	label890:
	label888:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label893
	movl $1,-328(%ebp)
	jmp label894
	label893:
	movl $0,-328(%ebp)
	label894:
	movl -328(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label895
	call inject_int
	jmp label896
	label895:
	cmpl $1,%eax
	jne label897
	call inject_bool
	jmp label898
	label897:
	cmpl $3,%eax
	jne label899
	call inject_big
	jmp label900
	label899:
	label900:
	label898:
	label896:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label901
	call inject_int
	jmp label902
	label901:
	cmpl $1,%eax
	jne label903
	call inject_bool
	jmp label904
	label903:
	cmpl $3,%eax
	jne label905
	call inject_big
	jmp label906
	label905:
	label906:
	label904:
	label902:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label907
	call inject_int
	jmp label908
	label907:
	cmpl $1,%eax
	jne label909
	call inject_bool
	jmp label910
	label909:
	cmpl $3,%eax
	jne label911
	call inject_big
	jmp label912
	label911:
	label912:
	label910:
	label908:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label913
	movl $1,-376(%ebp)
	jmp label914
	label913:
	movl $0,-376(%ebp)
	label914:
	movl -376(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label915
	call inject_int
	jmp label916
	label915:
	cmpl $1,%eax
	jne label917
	call inject_bool
	jmp label918
	label917:
	cmpl $3,%eax
	jne label919
	call inject_big
	jmp label920
	label919:
	label920:
	label918:
	label916:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label921
	movl -4(%ebp),%eax
	movl %eax,-232(%ebp)
	jmp label922
	label921:
	movl %ebx,%eax
	movl %eax,-232(%ebp)
	label922:
	addl $4,%esp
	movl -232(%ebp),%eax
	movl %eax,-4(%ebp)
	movl -4(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label923
	addl $4,%esp
	movl -12(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label925
	call project_int
	jmp label926
	label925:
	cmpl $1,%eax
	jne label927
	call project_bool
	jmp label928
	label927:
	cmpl $3,%eax
	jne label929
	call project_big
	jmp label930
	label929:
	label930:
	label928:
	label926:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -28(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label931
	call project_int
	jmp label932
	label931:
	cmpl $1,%eax
	jne label933
	call project_bool
	jmp label934
	label933:
	cmpl $3,%eax
	jne label935
	call project_big
	jmp label936
	label935:
	label936:
	label934:
	label932:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	pushl %eax
	pushl %ebx
	call add
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label937
	call inject_int
	jmp label938
	label937:
	cmpl $1,%eax
	jne label939
	call inject_bool
	jmp label940
	label939:
	cmpl $3,%eax
	jne label941
	call inject_big
	jmp label942
	label941:
	label942:
	label940:
	label938:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-220(%ebp)
	jmp label924
	label923:
	call type_error
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-220(%ebp)
	label924:
	movl -220(%ebp),%eax
	movl %eax,-56(%ebp)
	label862:
	movl -56(%ebp),%eax
	movl %eax,-76(%ebp)
	label800:
	movl -76(%ebp),%eax
	movl %eax,-244(%ebp)
	label738:
	movl -244(%ebp),%eax
	movl %eax,-240(%ebp)
	label676:
	movl -240(%ebp),%eax
	movl %eax,-36(%ebp)
	movl -92(%ebp),%eax
	movl %eax,-32(%ebp)
	movl -16(%ebp),%eax
	movl %eax,-20(%ebp)
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label943
	call inject_int
	jmp label944
	label943:
	cmpl $1,%eax
	jne label945
	call inject_bool
	jmp label946
	label945:
	cmpl $3,%eax
	jne label947
	call inject_big
	jmp label948
	label947:
	label948:
	label946:
	label944:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label949
	call inject_int
	jmp label950
	label949:
	cmpl $1,%eax
	jne label951
	call inject_bool
	jmp label952
	label951:
	cmpl $3,%eax
	jne label953
	call inject_big
	jmp label954
	label953:
	label954:
	label952:
	label950:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label955
	movl $1,-300(%ebp)
	jmp label956
	label955:
	movl $0,-300(%ebp)
	label956:
	movl -300(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label957
	call inject_int
	jmp label958
	label957:
	cmpl $1,%eax
	jne label959
	call inject_bool
	jmp label960
	label959:
	cmpl $3,%eax
	jne label961
	call inject_big
	jmp label962
	label961:
	label962:
	label960:
	label958:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label963
	call inject_int
	jmp label964
	label963:
	cmpl $1,%eax
	jne label965
	call inject_bool
	jmp label966
	label965:
	cmpl $3,%eax
	jne label967
	call inject_big
	jmp label968
	label967:
	label968:
	label966:
	label964:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label969
	call inject_int
	jmp label970
	label969:
	cmpl $1,%eax
	jne label971
	call inject_bool
	jmp label972
	label971:
	cmpl $3,%eax
	jne label973
	call inject_big
	jmp label974
	label973:
	label974:
	label972:
	label970:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label975
	movl $1,-380(%ebp)
	jmp label976
	label975:
	movl $0,-380(%ebp)
	label976:
	movl -380(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label977
	call inject_int
	jmp label978
	label977:
	cmpl $1,%eax
	jne label979
	call inject_bool
	jmp label980
	label979:
	cmpl $3,%eax
	jne label981
	call inject_big
	jmp label982
	label981:
	label982:
	label980:
	label978:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label983
	movl -4(%ebp),%eax
	movl %eax,-188(%ebp)
	jmp label984
	label983:
	movl %ebx,%eax
	movl %eax,-188(%ebp)
	label984:
	addl $4,%esp
	movl -188(%ebp),%eax
	movl %eax,-28(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label985
	addl $4,%esp
	movl -32(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label987
	call project_int
	jmp label988
	label987:
	cmpl $1,%eax
	jne label989
	call project_bool
	jmp label990
	label989:
	cmpl $3,%eax
	jne label991
	call project_big
	jmp label992
	label991:
	label992:
	label990:
	label988:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -20(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label993
	call project_int
	jmp label994
	label993:
	cmpl $1,%eax
	jne label995
	call project_bool
	jmp label996
	label995:
	cmpl $3,%eax
	jne label997
	call project_big
	jmp label998
	label997:
	label998:
	label996:
	label994:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	addl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label999
	call inject_int
	jmp label1000
	label999:
	cmpl $1,%eax
	jne label1001
	call inject_bool
	jmp label1002
	label1001:
	cmpl $3,%eax
	jne label1003
	call inject_big
	jmp label1004
	label1003:
	label1004:
	label1002:
	label1000:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-324(%ebp)
	jmp label986
	label985:
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1005
	call inject_int
	jmp label1006
	label1005:
	cmpl $1,%eax
	jne label1007
	call inject_bool
	jmp label1008
	label1007:
	cmpl $3,%eax
	jne label1009
	call inject_big
	jmp label1010
	label1009:
	label1010:
	label1008:
	label1006:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1011
	call inject_int
	jmp label1012
	label1011:
	cmpl $1,%eax
	jne label1013
	call inject_bool
	jmp label1014
	label1013:
	cmpl $3,%eax
	jne label1015
	call inject_big
	jmp label1016
	label1015:
	label1016:
	label1014:
	label1012:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1017
	movl $1,-172(%ebp)
	jmp label1018
	label1017:
	movl $0,-172(%ebp)
	label1018:
	movl -172(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1019
	call inject_int
	jmp label1020
	label1019:
	cmpl $1,%eax
	jne label1021
	call inject_bool
	jmp label1022
	label1021:
	cmpl $3,%eax
	jne label1023
	call inject_big
	jmp label1024
	label1023:
	label1024:
	label1022:
	label1020:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1025
	call inject_int
	jmp label1026
	label1025:
	cmpl $1,%eax
	jne label1027
	call inject_bool
	jmp label1028
	label1027:
	cmpl $3,%eax
	jne label1029
	call inject_big
	jmp label1030
	label1029:
	label1030:
	label1028:
	label1026:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1031
	call inject_int
	jmp label1032
	label1031:
	cmpl $1,%eax
	jne label1033
	call inject_bool
	jmp label1034
	label1033:
	cmpl $3,%eax
	jne label1035
	call inject_big
	jmp label1036
	label1035:
	label1036:
	label1034:
	label1032:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1037
	movl $1,-256(%ebp)
	jmp label1038
	label1037:
	movl $0,-256(%ebp)
	label1038:
	movl -256(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1039
	call inject_int
	jmp label1040
	label1039:
	cmpl $1,%eax
	jne label1041
	call inject_bool
	jmp label1042
	label1041:
	cmpl $3,%eax
	jne label1043
	call inject_big
	jmp label1044
	label1043:
	label1044:
	label1042:
	label1040:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1045
	movl -4(%ebp),%eax
	movl %eax,-104(%ebp)
	jmp label1046
	label1045:
	movl %ebx,%eax
	movl %eax,-104(%ebp)
	label1046:
	addl $4,%esp
	movl -104(%ebp),%eax
	movl %eax,-16(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1047
	addl $4,%esp
	movl -32(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1049
	call project_int
	jmp label1050
	label1049:
	cmpl $1,%eax
	jne label1051
	call project_bool
	jmp label1052
	label1051:
	cmpl $3,%eax
	jne label1053
	call project_big
	jmp label1054
	label1053:
	label1054:
	label1052:
	label1050:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -20(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1055
	call project_int
	jmp label1056
	label1055:
	cmpl $1,%eax
	jne label1057
	call project_bool
	jmp label1058
	label1057:
	cmpl $3,%eax
	jne label1059
	call project_big
	jmp label1060
	label1059:
	label1060:
	label1058:
	label1056:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	addl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1061
	call inject_int
	jmp label1062
	label1061:
	cmpl $1,%eax
	jne label1063
	call inject_bool
	jmp label1064
	label1063:
	cmpl $3,%eax
	jne label1065
	call inject_big
	jmp label1066
	label1065:
	label1066:
	label1064:
	label1062:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-292(%ebp)
	jmp label1048
	label1047:
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1067
	call inject_int
	jmp label1068
	label1067:
	cmpl $1,%eax
	jne label1069
	call inject_bool
	jmp label1070
	label1069:
	cmpl $3,%eax
	jne label1071
	call inject_big
	jmp label1072
	label1071:
	label1072:
	label1070:
	label1068:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1073
	call inject_int
	jmp label1074
	label1073:
	cmpl $1,%eax
	jne label1075
	call inject_bool
	jmp label1076
	label1075:
	cmpl $3,%eax
	jne label1077
	call inject_big
	jmp label1078
	label1077:
	label1078:
	label1076:
	label1074:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1079
	movl $1,-140(%ebp)
	jmp label1080
	label1079:
	movl $0,-140(%ebp)
	label1080:
	movl -140(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1081
	call inject_int
	jmp label1082
	label1081:
	cmpl $1,%eax
	jne label1083
	call inject_bool
	jmp label1084
	label1083:
	cmpl $3,%eax
	jne label1085
	call inject_big
	jmp label1086
	label1085:
	label1086:
	label1084:
	label1082:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1087
	call inject_int
	jmp label1088
	label1087:
	cmpl $1,%eax
	jne label1089
	call inject_bool
	jmp label1090
	label1089:
	cmpl $3,%eax
	jne label1091
	call inject_big
	jmp label1092
	label1091:
	label1092:
	label1090:
	label1088:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1093
	call inject_int
	jmp label1094
	label1093:
	cmpl $1,%eax
	jne label1095
	call inject_bool
	jmp label1096
	label1095:
	cmpl $3,%eax
	jne label1097
	call inject_big
	jmp label1098
	label1097:
	label1098:
	label1096:
	label1094:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1099
	movl $1,-260(%ebp)
	jmp label1100
	label1099:
	movl $0,-260(%ebp)
	label1100:
	movl -260(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1101
	call inject_int
	jmp label1102
	label1101:
	cmpl $1,%eax
	jne label1103
	call inject_bool
	jmp label1104
	label1103:
	cmpl $3,%eax
	jne label1105
	call inject_big
	jmp label1106
	label1105:
	label1106:
	label1104:
	label1102:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1107
	movl -4(%ebp),%eax
	movl %eax,-200(%ebp)
	jmp label1108
	label1107:
	movl %ebx,%eax
	movl %eax,-200(%ebp)
	label1108:
	addl $4,%esp
	movl -200(%ebp),%eax
	movl %eax,-12(%ebp)
	movl -12(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1109
	addl $4,%esp
	movl -32(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1111
	call project_int
	jmp label1112
	label1111:
	cmpl $1,%eax
	jne label1113
	call project_bool
	jmp label1114
	label1113:
	cmpl $3,%eax
	jne label1115
	call project_big
	jmp label1116
	label1115:
	label1116:
	label1114:
	label1112:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1117
	call project_int
	jmp label1118
	label1117:
	cmpl $1,%eax
	jne label1119
	call project_bool
	jmp label1120
	label1119:
	cmpl $3,%eax
	jne label1121
	call project_big
	jmp label1122
	label1121:
	label1122:
	label1120:
	label1118:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1123
	call inject_int
	jmp label1124
	label1123:
	cmpl $1,%eax
	jne label1125
	call inject_bool
	jmp label1126
	label1125:
	cmpl $3,%eax
	jne label1127
	call inject_big
	jmp label1128
	label1127:
	label1128:
	label1126:
	label1124:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-216(%ebp)
	jmp label1110
	label1109:
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1129
	call inject_int
	jmp label1130
	label1129:
	cmpl $1,%eax
	jne label1131
	call inject_bool
	jmp label1132
	label1131:
	cmpl $3,%eax
	jne label1133
	call inject_big
	jmp label1134
	label1133:
	label1134:
	label1132:
	label1130:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1135
	call inject_int
	jmp label1136
	label1135:
	cmpl $1,%eax
	jne label1137
	call inject_bool
	jmp label1138
	label1137:
	cmpl $3,%eax
	jne label1139
	call inject_big
	jmp label1140
	label1139:
	label1140:
	label1138:
	label1136:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1141
	movl $1,-68(%ebp)
	jmp label1142
	label1141:
	movl $0,-68(%ebp)
	label1142:
	movl -68(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1143
	call inject_int
	jmp label1144
	label1143:
	cmpl $1,%eax
	jne label1145
	call inject_bool
	jmp label1146
	label1145:
	cmpl $3,%eax
	jne label1147
	call inject_big
	jmp label1148
	label1147:
	label1148:
	label1146:
	label1144:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1149
	call inject_int
	jmp label1150
	label1149:
	cmpl $1,%eax
	jne label1151
	call inject_bool
	jmp label1152
	label1151:
	cmpl $3,%eax
	jne label1153
	call inject_big
	jmp label1154
	label1153:
	label1154:
	label1152:
	label1150:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1155
	call inject_int
	jmp label1156
	label1155:
	cmpl $1,%eax
	jne label1157
	call inject_bool
	jmp label1158
	label1157:
	cmpl $3,%eax
	jne label1159
	call inject_big
	jmp label1160
	label1159:
	label1160:
	label1158:
	label1156:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1161
	movl $1,-316(%ebp)
	jmp label1162
	label1161:
	movl $0,-316(%ebp)
	label1162:
	movl -316(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1163
	call inject_int
	jmp label1164
	label1163:
	cmpl $1,%eax
	jne label1165
	call inject_bool
	jmp label1166
	label1165:
	cmpl $3,%eax
	jne label1167
	call inject_big
	jmp label1168
	label1167:
	label1168:
	label1166:
	label1164:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1169
	movl -4(%ebp),%eax
	movl %eax,-248(%ebp)
	jmp label1170
	label1169:
	movl %ebx,%eax
	movl %eax,-248(%ebp)
	label1170:
	addl $4,%esp
	movl -248(%ebp),%eax
	movl %eax,-24(%ebp)
	movl -24(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1171
	addl $4,%esp
	movl -32(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1173
	call project_int
	jmp label1174
	label1173:
	cmpl $1,%eax
	jne label1175
	call project_bool
	jmp label1176
	label1175:
	cmpl $3,%eax
	jne label1177
	call project_big
	jmp label1178
	label1177:
	label1178:
	label1176:
	label1174:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -20(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1179
	call project_int
	jmp label1180
	label1179:
	cmpl $1,%eax
	jne label1181
	call project_bool
	jmp label1182
	label1181:
	cmpl $3,%eax
	jne label1183
	call project_big
	jmp label1184
	label1183:
	label1184:
	label1182:
	label1180:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	addl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1185
	call inject_int
	jmp label1186
	label1185:
	cmpl $1,%eax
	jne label1187
	call inject_bool
	jmp label1188
	label1187:
	cmpl $3,%eax
	jne label1189
	call inject_big
	jmp label1190
	label1189:
	label1190:
	label1188:
	label1186:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-144(%ebp)
	jmp label1172
	label1171:
	movl -32(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1191
	call inject_int
	jmp label1192
	label1191:
	cmpl $1,%eax
	jne label1193
	call inject_bool
	jmp label1194
	label1193:
	cmpl $3,%eax
	jne label1195
	call inject_big
	jmp label1196
	label1195:
	label1196:
	label1194:
	label1192:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1197
	call inject_int
	jmp label1198
	label1197:
	cmpl $1,%eax
	jne label1199
	call inject_bool
	jmp label1200
	label1199:
	cmpl $3,%eax
	jne label1201
	call inject_big
	jmp label1202
	label1201:
	label1202:
	label1200:
	label1198:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1203
	movl $1,-388(%ebp)
	jmp label1204
	label1203:
	movl $0,-388(%ebp)
	label1204:
	movl -388(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1205
	call inject_int
	jmp label1206
	label1205:
	cmpl $1,%eax
	jne label1207
	call inject_bool
	jmp label1208
	label1207:
	cmpl $3,%eax
	jne label1209
	call inject_big
	jmp label1210
	label1209:
	label1210:
	label1208:
	label1206:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1211
	call inject_int
	jmp label1212
	label1211:
	cmpl $1,%eax
	jne label1213
	call inject_bool
	jmp label1214
	label1213:
	cmpl $3,%eax
	jne label1215
	call inject_big
	jmp label1216
	label1215:
	label1216:
	label1214:
	label1212:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1217
	call inject_int
	jmp label1218
	label1217:
	cmpl $1,%eax
	jne label1219
	call inject_bool
	jmp label1220
	label1219:
	cmpl $3,%eax
	jne label1221
	call inject_big
	jmp label1222
	label1221:
	label1222:
	label1220:
	label1218:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1223
	movl $1,-252(%ebp)
	jmp label1224
	label1223:
	movl $0,-252(%ebp)
	label1224:
	movl -252(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1225
	call inject_int
	jmp label1226
	label1225:
	cmpl $1,%eax
	jne label1227
	call inject_bool
	jmp label1228
	label1227:
	cmpl $3,%eax
	jne label1229
	call inject_big
	jmp label1230
	label1229:
	label1230:
	label1228:
	label1226:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1231
	movl -4(%ebp),%eax
	movl %eax,-152(%ebp)
	jmp label1232
	label1231:
	movl %ebx,-152(%ebp)
	label1232:
	addl $4,%esp
	movl -152(%ebp),%eax
	movl %eax,-8(%ebp)
	movl -8(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1233
	addl $4,%esp
	movl -32(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label1235
	call project_int
	jmp label1236
	label1235:
	cmpl $1,%eax
	jne label1237
	call project_bool
	jmp label1238
	label1237:
	cmpl $3,%eax
	jne label1239
	call project_big
	jmp label1240
	label1239:
	label1240:
	label1238:
	label1236:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label1241
	call project_int
	jmp label1242
	label1241:
	cmpl $1,%eax
	jne label1243
	call project_bool
	jmp label1244
	label1243:
	cmpl $3,%eax
	jne label1245
	call project_big
	jmp label1246
	label1245:
	label1246:
	label1244:
	label1242:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	pushl %ebx
	pushl %eax
	call add
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label1247
	call inject_int
	jmp label1248
	label1247:
	cmpl $1,%eax
	jne label1249
	call inject_bool
	jmp label1250
	label1249:
	cmpl $3,%eax
	jne label1251
	call inject_big
	jmp label1252
	label1251:
	label1252:
	label1250:
	label1248:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-192(%ebp)
	jmp label1234
	label1233:
	call type_error
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-192(%ebp)
	label1234:
	movl -192(%ebp),%eax
	movl %eax,-144(%ebp)
	label1172:
	movl -144(%ebp),%eax
	movl %eax,-216(%ebp)
	label1110:
	movl -216(%ebp),%eax
	movl %eax,-292(%ebp)
	label1048:
	movl -292(%ebp),%eax
	movl %eax,-324(%ebp)
	label986:
	movl -324(%ebp),%eax
	movl %eax,-28(%ebp)
	movl -36(%ebp),%eax
	movl %eax,-16(%ebp)
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1253
	call inject_int
	jmp label1254
	label1253:
	cmpl $1,%eax
	jne label1255
	call inject_bool
	jmp label1256
	label1255:
	cmpl $3,%eax
	jne label1257
	call inject_big
	jmp label1258
	label1257:
	label1258:
	label1256:
	label1254:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1259
	call inject_int
	jmp label1260
	label1259:
	cmpl $1,%eax
	jne label1261
	call inject_bool
	jmp label1262
	label1261:
	cmpl $3,%eax
	jne label1263
	call inject_big
	jmp label1264
	label1263:
	label1264:
	label1262:
	label1260:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1265
	movl $1,-396(%ebp)
	jmp label1266
	label1265:
	movl $0,-396(%ebp)
	label1266:
	movl -396(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1267
	call inject_int
	jmp label1268
	label1267:
	cmpl $1,%eax
	jne label1269
	call inject_bool
	jmp label1270
	label1269:
	cmpl $3,%eax
	jne label1271
	call inject_big
	jmp label1272
	label1271:
	label1272:
	label1270:
	label1268:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1273
	call inject_int
	jmp label1274
	label1273:
	cmpl $1,%eax
	jne label1275
	call inject_bool
	jmp label1276
	label1275:
	cmpl $3,%eax
	jne label1277
	call inject_big
	jmp label1278
	label1277:
	label1278:
	label1276:
	label1274:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1279
	call inject_int
	jmp label1280
	label1279:
	cmpl $1,%eax
	jne label1281
	call inject_bool
	jmp label1282
	label1281:
	cmpl $3,%eax
	jne label1283
	call inject_big
	jmp label1284
	label1283:
	label1284:
	label1282:
	label1280:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1285
	movl $1,-308(%ebp)
	jmp label1286
	label1285:
	movl $0,-308(%ebp)
	label1286:
	movl -308(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1287
	call inject_int
	jmp label1288
	label1287:
	cmpl $1,%eax
	jne label1289
	call inject_bool
	jmp label1290
	label1289:
	cmpl $3,%eax
	jne label1291
	call inject_big
	jmp label1292
	label1291:
	label1292:
	label1290:
	label1288:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1293
	movl -4(%ebp),%eax
	movl %eax,-360(%ebp)
	jmp label1294
	label1293:
	movl %ebx,%eax
	movl %eax,-360(%ebp)
	label1294:
	addl $4,%esp
	movl -360(%ebp),%eax
	movl %eax,-24(%ebp)
	movl -24(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1295
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1297
	call project_int
	jmp label1298
	label1297:
	cmpl $1,%eax
	jne label1299
	call project_bool
	jmp label1300
	label1299:
	cmpl $3,%eax
	jne label1301
	call project_big
	jmp label1302
	label1301:
	label1302:
	label1300:
	label1298:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1303
	call project_int
	jmp label1304
	label1303:
	cmpl $1,%eax
	jne label1305
	call project_bool
	jmp label1306
	label1305:
	cmpl $3,%eax
	jne label1307
	call project_big
	jmp label1308
	label1307:
	label1308:
	label1306:
	label1304:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1309
	call inject_int
	jmp label1310
	label1309:
	cmpl $1,%eax
	jne label1311
	call inject_bool
	jmp label1312
	label1311:
	cmpl $3,%eax
	jne label1313
	call inject_big
	jmp label1314
	label1313:
	label1314:
	label1312:
	label1310:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-400(%ebp)
	jmp label1296
	label1295:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1315
	call inject_int
	jmp label1316
	label1315:
	cmpl $1,%eax
	jne label1317
	call inject_bool
	jmp label1318
	label1317:
	cmpl $3,%eax
	jne label1319
	call inject_big
	jmp label1320
	label1319:
	label1320:
	label1318:
	label1316:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1321
	call inject_int
	jmp label1322
	label1321:
	cmpl $1,%eax
	jne label1323
	call inject_bool
	jmp label1324
	label1323:
	cmpl $3,%eax
	jne label1325
	call inject_big
	jmp label1326
	label1325:
	label1326:
	label1324:
	label1322:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1327
	movl $1,-84(%ebp)
	jmp label1328
	label1327:
	movl $0,-84(%ebp)
	label1328:
	movl -84(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1329
	call inject_int
	jmp label1330
	label1329:
	cmpl $1,%eax
	jne label1331
	call inject_bool
	jmp label1332
	label1331:
	cmpl $3,%eax
	jne label1333
	call inject_big
	jmp label1334
	label1333:
	label1334:
	label1332:
	label1330:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-8(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1335
	call inject_int
	jmp label1336
	label1335:
	cmpl $1,%eax
	jne label1337
	call inject_bool
	jmp label1338
	label1337:
	cmpl $3,%eax
	jne label1339
	call inject_big
	jmp label1340
	label1339:
	label1340:
	label1338:
	label1336:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1341
	call inject_int
	jmp label1342
	label1341:
	cmpl $1,%eax
	jne label1343
	call inject_bool
	jmp label1344
	label1343:
	cmpl $3,%eax
	jne label1345
	call inject_big
	jmp label1346
	label1345:
	label1346:
	label1344:
	label1342:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1347
	movl $1,-160(%ebp)
	jmp label1348
	label1347:
	movl $0,-160(%ebp)
	label1348:
	movl -160(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1349
	call inject_int
	jmp label1350
	label1349:
	cmpl $1,%eax
	jne label1351
	call inject_bool
	jmp label1352
	label1351:
	cmpl $3,%eax
	jne label1353
	call inject_big
	jmp label1354
	label1353:
	label1354:
	label1352:
	label1350:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -8(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1355
	movl -4(%ebp),%eax
	movl %eax,-228(%ebp)
	jmp label1356
	label1355:
	movl %ebx,%eax
	movl %eax,-228(%ebp)
	label1356:
	addl $4,%esp
	movl -228(%ebp),%eax
	movl %eax,-12(%ebp)
	movl -12(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1357
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1359
	call project_int
	jmp label1360
	label1359:
	cmpl $1,%eax
	jne label1361
	call project_bool
	jmp label1362
	label1361:
	cmpl $3,%eax
	jne label1363
	call project_big
	jmp label1364
	label1363:
	label1364:
	label1362:
	label1360:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -16(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1365
	call project_int
	jmp label1366
	label1365:
	cmpl $1,%eax
	jne label1367
	call project_bool
	jmp label1368
	label1367:
	cmpl $3,%eax
	jne label1369
	call project_big
	jmp label1370
	label1369:
	label1370:
	label1368:
	label1366:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	addl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1371
	call inject_int
	jmp label1372
	label1371:
	cmpl $1,%eax
	jne label1373
	call inject_bool
	jmp label1374
	label1373:
	cmpl $3,%eax
	jne label1375
	call inject_big
	jmp label1376
	label1375:
	label1376:
	label1374:
	label1372:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-336(%ebp)
	jmp label1358
	label1357:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1377
	call inject_int
	jmp label1378
	label1377:
	cmpl $1,%eax
	jne label1379
	call inject_bool
	jmp label1380
	label1379:
	cmpl $3,%eax
	jne label1381
	call inject_big
	jmp label1382
	label1381:
	label1382:
	label1380:
	label1378:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1383
	call inject_int
	jmp label1384
	label1383:
	cmpl $1,%eax
	jne label1385
	call inject_bool
	jmp label1386
	label1385:
	cmpl $3,%eax
	jne label1387
	call inject_big
	jmp label1388
	label1387:
	label1388:
	label1386:
	label1384:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1389
	movl $1,-236(%ebp)
	jmp label1390
	label1389:
	movl $0,-236(%ebp)
	label1390:
	movl -236(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1391
	call inject_int
	jmp label1392
	label1391:
	cmpl $1,%eax
	jne label1393
	call inject_bool
	jmp label1394
	label1393:
	cmpl $3,%eax
	jne label1395
	call inject_big
	jmp label1396
	label1395:
	label1396:
	label1394:
	label1392:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1397
	call inject_int
	jmp label1398
	label1397:
	cmpl $1,%eax
	jne label1399
	call inject_bool
	jmp label1400
	label1399:
	cmpl $3,%eax
	jne label1401
	call inject_big
	jmp label1402
	label1401:
	label1402:
	label1400:
	label1398:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $0,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1403
	call inject_int
	jmp label1404
	label1403:
	cmpl $1,%eax
	jne label1405
	call inject_bool
	jmp label1406
	label1405:
	cmpl $3,%eax
	jne label1407
	call inject_big
	jmp label1408
	label1407:
	label1408:
	label1406:
	label1404:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1409
	movl $1,-268(%ebp)
	jmp label1410
	label1409:
	movl $0,-268(%ebp)
	label1410:
	movl -268(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1411
	call inject_int
	jmp label1412
	label1411:
	cmpl $1,%eax
	jne label1413
	call inject_bool
	jmp label1414
	label1413:
	cmpl $3,%eax
	jne label1415
	call inject_big
	jmp label1416
	label1415:
	label1416:
	label1414:
	label1412:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1417
	movl -4(%ebp),%eax
	movl %eax,-288(%ebp)
	jmp label1418
	label1417:
	movl %ebx,%eax
	movl %eax,-288(%ebp)
	label1418:
	addl $4,%esp
	movl -288(%ebp),%eax
	movl %eax,-20(%ebp)
	movl -20(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1419
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1421
	call project_int
	jmp label1422
	label1421:
	cmpl $1,%eax
	jne label1423
	call project_bool
	jmp label1424
	label1423:
	cmpl $3,%eax
	jne label1425
	call project_big
	jmp label1426
	label1425:
	label1426:
	label1424:
	label1422:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1427
	call project_int
	jmp label1428
	label1427:
	cmpl $1,%eax
	jne label1429
	call project_bool
	jmp label1430
	label1429:
	cmpl $3,%eax
	jne label1431
	call project_big
	jmp label1432
	label1431:
	label1432:
	label1430:
	label1428:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1433
	call inject_int
	jmp label1434
	label1433:
	cmpl $1,%eax
	jne label1435
	call inject_bool
	jmp label1436
	label1435:
	cmpl $3,%eax
	jne label1437
	call inject_big
	jmp label1438
	label1437:
	label1438:
	label1436:
	label1434:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-180(%ebp)
	jmp label1420
	label1419:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1439
	call inject_int
	jmp label1440
	label1439:
	cmpl $1,%eax
	jne label1441
	call inject_bool
	jmp label1442
	label1441:
	cmpl $3,%eax
	jne label1443
	call inject_big
	jmp label1444
	label1443:
	label1444:
	label1442:
	label1440:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1445
	call inject_int
	jmp label1446
	label1445:
	cmpl $1,%eax
	jne label1447
	call inject_bool
	jmp label1448
	label1447:
	cmpl $3,%eax
	jne label1449
	call inject_big
	jmp label1450
	label1449:
	label1450:
	label1448:
	label1446:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1451
	movl $1,-48(%ebp)
	jmp label1452
	label1451:
	movl $0,-48(%ebp)
	label1452:
	movl -48(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1453
	call inject_int
	jmp label1454
	label1453:
	cmpl $1,%eax
	jne label1455
	call inject_bool
	jmp label1456
	label1455:
	cmpl $3,%eax
	jne label1457
	call inject_big
	jmp label1458
	label1457:
	label1458:
	label1456:
	label1454:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1459
	call inject_int
	jmp label1460
	label1459:
	cmpl $1,%eax
	jne label1461
	call inject_bool
	jmp label1462
	label1461:
	cmpl $3,%eax
	jne label1463
	call inject_big
	jmp label1464
	label1463:
	label1464:
	label1462:
	label1460:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $1,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1465
	call inject_int
	jmp label1466
	label1465:
	cmpl $1,%eax
	jne label1467
	call inject_bool
	jmp label1468
	label1467:
	cmpl $3,%eax
	jne label1469
	call inject_big
	jmp label1470
	label1469:
	label1470:
	label1468:
	label1466:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1471
	movl $1,-344(%ebp)
	jmp label1472
	label1471:
	movl $0,-344(%ebp)
	label1472:
	movl -344(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1473
	call inject_int
	jmp label1474
	label1473:
	cmpl $1,%eax
	jne label1475
	call inject_bool
	jmp label1476
	label1475:
	cmpl $3,%eax
	jne label1477
	call inject_big
	jmp label1478
	label1477:
	label1478:
	label1476:
	label1474:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1479
	movl -4(%ebp),%eax
	movl %eax,-176(%ebp)
	jmp label1480
	label1479:
	movl %ebx,%eax
	movl %eax,-176(%ebp)
	label1480:
	addl $4,%esp
	movl -176(%ebp),%eax
	movl %eax,-8(%ebp)
	movl -8(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1481
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1483
	call project_int
	jmp label1484
	label1483:
	cmpl $1,%eax
	jne label1485
	call project_bool
	jmp label1486
	label1485:
	cmpl $3,%eax
	jne label1487
	call project_big
	jmp label1488
	label1487:
	label1488:
	label1486:
	label1484:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1489
	call project_int
	jmp label1490
	label1489:
	cmpl $1,%eax
	jne label1491
	call project_bool
	jmp label1492
	label1491:
	cmpl $3,%eax
	jne label1493
	call project_big
	jmp label1494
	label1493:
	label1494:
	label1492:
	label1490:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	addl %eax,%ebx
	movl %ebx,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1495
	call inject_int
	jmp label1496
	label1495:
	cmpl $1,%eax
	jne label1497
	call inject_bool
	jmp label1498
	label1497:
	cmpl $3,%eax
	jne label1499
	call inject_big
	jmp label1500
	label1499:
	label1500:
	label1498:
	label1496:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-356(%ebp)
	jmp label1482
	label1481:
	movl -28(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1501
	call inject_int
	jmp label1502
	label1501:
	cmpl $1,%eax
	jne label1503
	call inject_bool
	jmp label1504
	label1503:
	cmpl $3,%eax
	jne label1505
	call inject_big
	jmp label1506
	label1505:
	label1506:
	label1504:
	label1502:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1507
	call inject_int
	jmp label1508
	label1507:
	cmpl $1,%eax
	jne label1509
	call inject_bool
	jmp label1510
	label1509:
	cmpl $3,%eax
	jne label1511
	call inject_big
	jmp label1512
	label1511:
	label1512:
	label1510:
	label1508:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %ebx,%ebx
	cmpl %eax,%ebx
	jne label1513
	movl $1,-64(%ebp)
	jmp label1514
	label1513:
	movl $0,-64(%ebp)
	label1514:
	movl -64(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1515
	call inject_int
	jmp label1516
	label1515:
	cmpl $1,%eax
	jne label1517
	call inject_bool
	jmp label1518
	label1517:
	cmpl $3,%eax
	jne label1519
	call inject_big
	jmp label1520
	label1519:
	label1520:
	label1518:
	label1516:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,-4(%ebp)
	movl -16(%ebp),%eax
	pushl %eax
	call tag
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1521
	call inject_int
	jmp label1522
	label1521:
	cmpl $1,%eax
	jne label1523
	call inject_bool
	jmp label1524
	label1523:
	cmpl $3,%eax
	jne label1525
	call inject_big
	jmp label1526
	label1525:
	label1526:
	label1524:
	label1522:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl $3,%eax
	pushl %eax
	movl $0,%eax
	cmpl $0,%eax
	jne label1527
	call inject_int
	jmp label1528
	label1527:
	cmpl $1,%eax
	jne label1529
	call inject_bool
	jmp label1530
	label1529:
	cmpl $3,%eax
	jne label1531
	call inject_big
	jmp label1532
	label1531:
	label1532:
	label1530:
	label1528:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	cmpl %ebx,%eax
	jne label1533
	movl $1,-212(%ebp)
	jmp label1534
	label1533:
	movl $0,-212(%ebp)
	label1534:
	movl -212(%ebp),%eax
	movl %eax,%eax
	pushl %eax
	movl $1,%eax
	cmpl $0,%eax
	jne label1535
	call inject_int
	jmp label1536
	label1535:
	cmpl $1,%eax
	jne label1537
	call inject_bool
	jmp label1538
	label1537:
	cmpl $3,%eax
	jne label1539
	call inject_big
	jmp label1540
	label1539:
	label1540:
	label1538:
	label1536:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -4(%ebp),%eax
	movl %eax,-4(%ebp)
	movl %ebx,%ebx
	pushl -4(%ebp)
	call is_true
	cmpl $0,%eax
	jne label1541
	movl -4(%ebp),%eax
	movl %eax,-44(%ebp)
	jmp label1542
	label1541:
	movl %ebx,%eax
	movl %eax,-44(%ebp)
	label1542:
	addl $4,%esp
	movl -44(%ebp),%eax
	movl %eax,-4(%ebp)
	movl -4(%ebp),%eax
	pushl %eax
	call is_true
	cmpl $1,%eax
	jne label1543
	addl $4,%esp
	movl -28(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label1545
	call project_int
	jmp label1546
	label1545:
	cmpl $1,%eax
	jne label1547
	call project_bool
	jmp label1548
	label1547:
	cmpl $3,%eax
	jne label1549
	call project_big
	jmp label1550
	label1549:
	label1550:
	label1548:
	label1546:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%ebx
	movl -16(%ebp),%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label1551
	call project_int
	jmp label1552
	label1551:
	cmpl $1,%eax
	jne label1553
	call project_bool
	jmp label1554
	label1553:
	cmpl $3,%eax
	jne label1555
	call project_big
	jmp label1556
	label1555:
	label1556:
	label1554:
	label1552:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %ebx,%ebx
	movl %eax,%eax
	pushl %eax
	pushl %ebx
	call add
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	pushl %eax
	movl $3,%eax
	cmpl $0,%eax
	jne label1557
	call inject_int
	jmp label1558
	label1557:
	cmpl $1,%eax
	jne label1559
	call inject_bool
	jmp label1560
	label1559:
	cmpl $3,%eax
	jne label1561
	call inject_big
	jmp label1562
	label1561:
	label1562:
	label1560:
	label1558:
	movl %eax,%eax
	addl $4,%esp
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-368(%ebp)
	jmp label1544
	label1543:
	call type_error
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,%eax
	movl %eax,-368(%ebp)
	label1544:
	movl -368(%ebp),%eax
	movl %eax,-356(%ebp)
	label1482:
	movl -356(%ebp),%eax
	movl %eax,-180(%ebp)
	label1420:
	movl -180(%ebp),%eax
	movl %eax,-336(%ebp)
	label1358:
	movl -336(%ebp),%eax
	movl %eax,-400(%ebp)
	label1296:
	movl -400(%ebp),%eax
	movl %eax,%eax
	movl -36(%ebp),%eax
	pushl %eax
	call print_any
	addl $4,%esp
	leave
	ret
