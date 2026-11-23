using System;
using System.Collections.Generic;
using UnityEngine;

namespace Inven.Item.Attribute
{
	[Serializable]
	public class ItemAttribute
	{
		[Serializable]
		public enum Type
		{
			ClipBuff = 0
		}

		[SerializeReference]
		private List<ItemAttributeBase> list;

		public void AddClipBuff()
		{
		}

		public bool TryGet<T>(out T result) where T : ItemAttributeBase
		{
			result = null;
			return false;
		}
	}
}
