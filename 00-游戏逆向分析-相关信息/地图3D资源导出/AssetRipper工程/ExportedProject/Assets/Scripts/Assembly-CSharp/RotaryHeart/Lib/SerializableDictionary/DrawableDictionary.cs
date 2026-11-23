using UnityEngine;

namespace RotaryHeart.Lib.SerializableDictionary
{
	public abstract class DrawableDictionary
	{
		[HideInInspector]
		public ReorderableList reorderableList;

		[HideInInspector]
		public RequiredReferences reqReferences;

		public bool isExpanded;
	}
}
