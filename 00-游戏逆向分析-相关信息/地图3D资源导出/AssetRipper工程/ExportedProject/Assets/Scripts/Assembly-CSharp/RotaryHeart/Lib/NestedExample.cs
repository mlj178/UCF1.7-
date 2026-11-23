using System;
using UnityEngine;

namespace RotaryHeart.Lib
{
	[Serializable]
	public class NestedExample
	{
		public GameObject prefab;

		public float speed;

		public Color color;

		public Nested2Dict deepNested;
	}
}
